import torch
import transformers
from langchain.llms import HuggingFacePipeline
from torch import bfloat16, cuda
from transformers import (AutoModelForCausalLM, AutoTokenizer,
                          BitsAndBytesConfig, pipeline)

from taitriscore.basebot.base_gpt_api import BaseGPTAPI
from taitriscore.basebot.basebot_utils import (CostHandler, Costs,
                                               RequestRateLimiter, retry)
from taitriscore.config import CONFIG
from taitriscore.utils.token_counter import (TOKEN_COSTS, count_message_tokens,
                                             count_string_tokens)


class LLAMAAPI(BaseGPTAPI, RequestRateLimiter):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            CONFIG.llama_model_name, use_auth_token=CONFIG.HUGGINGFACE_API_KEY
        )
        if CONFIG.llama_model_name == "meta-llama/Llama-2-7b-chat-hf":
            self.bnb_config = transformers.BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=bfloat16,
            )
            model_config = transformers.AutoConfig.from_pretrained(
                CONFIG.llama_model_name, use_auth_token=CONFIG.HUGGINGFACE_API_KEY
            )
            self.model = transformers.AutoModelForCausalLM.from_pretrained(
                CONFIG.llama_model_name,
                trust_remote_code=True,
                load_in_4bit=True,
                config=model_config,
                quantization_config=bnb_config,
                device_map="auto",
                use_auth_token=CONFIG.HUGGINGFACE_API_KEY,
            )
        else:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                CONFIG.llama_model_name,
                quantization_config=self.bnb_config,
                trust_remote_code=True,
            )
            self.model.config.use_cache = False

        self.model = self.model.eval()
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=100,
            early_stopping=True,
            no_repeat_ngram_size=2,
        )
        self.llm = HuggingFacePipeline(pipeline=self.pipe)
        self._cost_manager = CostHandler()
        self.rpm = CONFIG.rpm
        RequestRateLimiter.__init__(self, rpm=self.rpm)
        super().__init__()

    def _calc_usage(self, messages, rsp):
        usage = {}
        if CONFIG.calc_usage:
            prompt_tokens = count_message_tokens(messages, CONFIG.llama_model_name)
            completion_tokens = count_string_tokens(rsp, CONFIG.llama_model_name)
            usage["prompt_tokens"] = prompt_tokens
            usage["completion_tokens"] = completion_tokens
        return usage

    def ask(self, prompt="Can you tell me what you know about Influencers Marketing?"):
        messages = [self._default_system_msg(), self._user_msg(prompt)]
        # res = self.llm(prompt=messages)
        res = self.llm(prompt=prompt)
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
        # res = self.llm(prompt=messages)
        res = self.llm(prompt=prompt)
        usage = self._calc_usage(prompt, res)
        self._update_costs(usage)
        return res

    def _update_costs(self, usage: dict):
        if CONFIG.update_costs:
            prompt_tokens = int(usage["prompt_tokens"])
            completion_tokens = int(usage["completion_tokens"])
            self._cost_manager.update_cost(
                prompt_tokens, completion_tokens, CONFIG.llama_model_name
            )

    def get_costs(self) -> Costs:
        return self._cost_manager.get_costs()
