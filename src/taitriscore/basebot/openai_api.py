import openai

from taitriscore.basebot.base_gpt_api import BaseGPTAPI
from taitriscore.basebot.basebot_utils import (CostHandler, Costs,
                                               RequestRateLimiter, retry)
from taitriscore.config import CONFIG
from taitriscore.utils.token_counter import (TOKEN_COSTS, count_message_tokens,
                                             count_string_tokens)


class OpenAIAPI(BaseGPTAPI, RequestRateLimiter):
    def __init__(self):
        self.__init_openai(CONFIG)
        self.llm = openai
        self.model = CONFIG.openai_model
        self._cost_manager = CostHandler()
        RequestRateLimiter.__init__(self, rpm=self.rpm)
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
