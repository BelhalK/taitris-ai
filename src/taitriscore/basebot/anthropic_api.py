import abc
import asyncio
import time
from functools import wraps
from typing import NamedTuple

import torch
from anthropic import AsyncAnthropic
from anthropic.types import Message, Usage

from taitriscore.basebot.base_gpt_api import BaseGPTAPI
from taitriscore.config import CONFIG, Singleton
from taitriscore.logs import logger
from taitriscore.utils.token_counter import (TOKEN_COSTS, count_message_tokens,
                                             count_string_tokens)


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


class RequestRateLimiter:
    def __init__(self, rpm):
        self.last_call_time = 0
        self.interval = 1.1 * 60 / rpm
        self.rpm = rpm

    def split_batches(self, batch):
        return [batch[i : i + self.rpm] for i in range(0, len(batch), self.rpm)]

    async def wait_if_needed(self, num_requests):
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


class AnthropicAPI(BaseGPTAPI, RequestRateLimiter):
    def __init__(self, config: LLMConfig):
        self.config = config
        self.__init_anthropic()

    def __init_anthropic(self, config):
        self.model = self.config.anthropic_model
        self.aclient: AsyncAnthropic = AsyncAnthropic(
            api_key=CONFIG.anthropic_api_key, base_url=CONFIG.anthropic_api_base
        )
        self.rpm = CONFIG.rpm

    def _const_kwargs(self, messages: list[dict], stream: bool = False) -> dict:
        kwargs = {
            "model": self.model,
            "messages": messages,
            "max_tokens": CONFIG.max_tokens_rsp,
        }
        if self.use_system_prompt:
            if messages[0]["role"] == "system":
                kwargs["messages"] = messages[1:]
                kwargs["system"] = messages[0]["content"]
        return kwargs

    def _update_costs(
        self, usage: Usage, model: str = None, local_calc_usage: bool = True
    ):
        usage = {
            "prompt_tokens": usage.input_tokens,
            "completion_tokens": usage.output_tokens,
        }
        super()._update_costs(usage, model)

    def get_choice_text(self, resp: Message) -> str:
        return resp.content[0].text

    async def aask(
        self, messages: list[dict], timeout: int = USE_CONFIG_TIMEOUT
    ) -> Message:
        resp: Message = await self.aclient.messages.create(
            **self._const_kwargs(messages)
        )
        self._update_costs(resp.usage, self.model)
        return resp
