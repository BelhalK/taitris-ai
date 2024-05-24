import abc
import asyncio
import pdb
import time
from functools import wraps
from typing import NamedTuple

import openai
import torch

from taitriscore.basebot.base_gpt_api import BaseGPTAPI
from taitriscore.config import CONFIG, Singleton
from taitriscore.logs import logger
from taitriscore.utils.token_counter import (
    TOKEN_COSTS,
    count_message_tokens,
    count_string_tokens,
)


def retry(max_retries):
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return await f(*args, **kwargs)
                except Exception:
                    if i == max_retries - 1:
                        raise
                    await asyncio.sleep(2**i)

        return wrapper

    return decorator


class RequestRequestRateLimiter:
    """
    A class to enforce rate limits on API requests.

    Attributes:
        rpm (int): The number of requests allowed per minute.
        last_call_time (float): The time when the last request was made.
        interval (float): The minimum interval between requests in seconds.

    Methods:
        split_batches(batch):
            Splits a batch of requests into smaller batches according to the rate limit.
        wait_if_needed(num_requests):
            Waits if necessary to ensure the rate limit is not exceeded.
    """

    def __init__(self, rpm):
        """
        Initializes the RequestRequestRateLimiter with the specified requests per minute (rpm).

        Args:
            rpm (int): The number of requests allowed per minute.
        """
        self.last_call_time = 0
        self.interval = 1.1 * 60 / rpm
        self.rpm = rpm

    def split_batches(self, batch):
        """
        Splits a batch of requests into smaller batches according to the rate limit.

        Args:
            batch (list): The list of requests to be split into batches.

        Returns:
            list: A list of smaller batches of requests.
        """
        return [batch[i : i + self.rpm] for i in range(0, len(batch), self.rpm)]

    async def wait_if_needed(self, num_requests):
        """
        Waits if necessary to ensure the rate limit is not exceeded.

        Args:
            num_requests (int): The number of requests to be made.

        Logs:
            Info: Logs the remaining time to sleep if rate limit is exceeded.
        """
        current_time = time.time()
        elapsed_time = current_time - self.last_call_time

        if elapsed_time < self.interval * num_requests:
            remaining_time = self.interval * num_requests - elapsed_time
            logger.info(f"sleep {remaining_time}")
            await asyncio.sleep(remaining_time)

        self.last_call_time = time.time()


class Costs(NamedTuple):
    total_prompt_tokens: int
    total_completion_tokens: int
    total_cost: float
    total_budget: float


class CostHandler(metaclass=Singleton):
    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0
        self.total_budget = 0

    def update_cost(self, prompt_tokens, completion_tokens, model):
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        cost = (
            prompt_tokens * TOKEN_COSTS[model]["prompt"]
            + completion_tokens * TOKEN_COSTS[model]["completion"]
        ) / 1000
        self.total_cost += cost
        logger.info(
            f"Total running cost: ${self.total_cost:.3f} | Max budget: ${CONFIG.max_budget:.3f} | "
            f"Current cost: ${cost:.3f}, {prompt_tokens}, {completion_tokens}"
        )
        CONFIG.total_cost = self.total_cost

    def get_total_prompt_tokens(self):
        return self.total_prompt_tokens

    def get_total_completion_tokens(self):
        return self.total_completion_tokens

    def get_total_cost(self):
        return self.total_cost

    def get_costs(self) -> Costs:
        return Costs(
            self.total_prompt_tokens,
            self.total_completion_tokens,
            self.total_cost,
            self.total_budget,
        )


class OpenAIAPI(BaseGPTAPI, RequestRequestRateLimiter):
    def __init__(self):
        self.__init_openai(CONFIG)
        self.llm = openai
        self.model = CONFIG.openai_model
        self._cost_manager = CostHandler()
        RequestRequestRateLimiter.__init__(self, rpm=self.rpm)
        super().__init__()

    def __init_openai(self, config):
        openai.api_key = CONFIG.openai_api_key
        if config.openai_api_base:
            openai.api_base = config.openai_api_base
        self.rpm = CONFIG.rpm

    def _cons_kwargs(self, messages):
        kwargs = {
            "model": self.model,
            "messages": messages,
            "max_tokens": CONFIG.max_tokens_rsp,
            "n": 1,
            "stop": None,
            "temperature": 0.3,
        }
        return kwargs

    def _calc_usage(self, messages, rsp):
        usage = {}
        if CONFIG.calc_usage:
            prompt_tokens = count_message_tokens(messages, self.model)
            completion_tokens = count_string_tokens(rsp, self.model)
            usage["prompt_tokens"] = prompt_tokens
            usage["completion_tokens"] = completion_tokens
        return usage

    def _call_chat(self, messages):
        # tmp_input = self._cons_kwargs(messages)
        # res = self.llm.ChatCompletion.create(**tmp_input)

        # res = self.llm.ChatCompletion.create(**self._cons_kwargs(messages))

        res = {
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "all good."},
                    "logprobs": "null",
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 102,
                "completion_tokens": 389,
                "total_tokens": 491,
            },
            "system_fingerprint": "null",
        }
        return res

    def ask(self, prompt="Can you tell me what you know about Influencers Marketing?"):
        messages = [self._default_system_msg(), self._user_msg(prompt)]
        res = self._call_chat(messages)
        usage = self._calc_usage(prompt, res)
        self._update_costs(usage)
        return res

    async def aask(
        self,
        prompt="Can you tell me what you know about Influencers Marketing?",
        system_msgs=None,
    ):
        if system_msgs:
            messages = self._system_msgs(system_msgs) + [self._user_msg(prompt)]
        else:
            messages = [self._default_system_msg(), self._user_msg(prompt)]
        res = self._call_chat(messages)
        usage = self._calc_usage(prompt, res)
        self._update_costs(usage)
        return res

    def _update_costs(self, usage: dict):
        if CONFIG.update_costs:
            prompt_tokens = int(usage["prompt_tokens"])
            completion_tokens = int(usage["completion_tokens"])
            self._cost_manager.update_cost(prompt_tokens, completion_tokens, self.model)

    def get_costs(self) -> Costs:
        return self._cost_manager.get_costs()
