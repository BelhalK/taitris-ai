from taitriscore.config import CONFIG

if CONFIG.platform == 'OPENAI':
    from taitriscore.basebot.openai_api import OpenAIAPI as LLM
elif CONFIG.platform == 'LLAMAV2':
    from taitriscore.basebot.llama_api import LLAMAAPI as LLM
elif CONFIG.platform == 'ANTHROPIC':
    from taitriscore.basebot.anthropic_api import AnthropicAPI as LLM
else:
    raise ValueError(f"Unsupported platform type: {CONFIG.platform}")


DEFAULT_LLM = LLM()
