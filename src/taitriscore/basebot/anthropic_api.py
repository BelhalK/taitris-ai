from anthropic import AsyncAnthropic
from anthropic.types import Message, Usage

from taitriscore.basebot.base_gpt_api import BaseGPTAPI
from taitriscore.basebot.basebot_utils import (CostHandler, Costs,
                                               RequestRateLimiter, retry)
from taitriscore.config import CONFIG, Singleton
from taitriscore.utils.token_counter import (TOKEN_COSTS, count_message_tokens,
                                             count_string_tokens)


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
