import abc
import os
import pdb
import re
import yaml
from dotenv import load_dotenv
from pathlib import Path

from taitriscore.const import PROJECT_ROOT, ENV_ROOT
from taitriscore.logs import logger
from taitriscore.tools import SearchEngineType, WebBrowserEngineType

# Load .env file
dotenv_path = ENV_ROOT / ".env"
load_dotenv(dotenv_path=dotenv_path)

class Singleton(abc.ABCMeta, type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class NotConfiguredException(Exception):
    def __init__(self, message="The required configuration is not set"):
        self.message = message
        super().__init__(self.message)

class Config(metaclass=Singleton):
    _instance = None
    key_yaml_file = PROJECT_ROOT / "taitriscore/config/key.yaml"
    default_yaml_file = PROJECT_ROOT / "taitriscore/config/config.yaml"

    def __init__(self, yaml_file=default_yaml_file):
        self._configs = {}
        self._init_with_config_files_and_env(self._configs, yaml_file)
        logger.info("Config loading done.")
        # Initialization of settings
        self.load_settings()

    def _init_with_config_files_and_env(self, configs: dict, yaml_file):
        configs.update(os.environ)

        for _yaml_file in [yaml_file, self.default_yaml_file]:
            if not _yaml_file.exists():
                continue

            with open(_yaml_file, "r", encoding="utf-8") as file:
                yaml_data = yaml.safe_load(file)
                if not yaml_data:
                    continue
                self._process_yaml_env(yaml_data)
                configs.update(yaml_data)

    def _process_yaml_env(self, yaml_data):
        pattern = re.compile(r'\$\{([^}]+)\}')
        for key, value in yaml_data.items():
            if isinstance(value, str):
                yaml_data[key] = pattern.sub(lambda x: os.environ.get(x.group(1), ''), value)

    def _get(self, key, default=None):
        return self._configs.get(key, default)

    def get(self, key, *args, **kwargs):
        value = self._get(key, *args, **kwargs)
        if value is None:
            raise ValueError(
                f"Key '{key}' not found in environment variables or in the YAML file"
            )
        return value

    def load_settings(self):
        # Load and set all config values
        self.max_tokens_rsp = self._get("MAX_TOKENS", 2048)
        self.platform = self._get("PLATFORM")
        self.anthropic_api_key = self._get("ANTHROPIC_API_KEY")
        self.anthropic_api_base = self._get("ANTHROPIC_API_BASE")
        self.anthropic_model = self._get("ANTHROPIC_MODEL")
        self.serpapi_api_key = self._get("SERPAPI_API_KEY")
        self.openai_api_key = self._get("OPENAI_API_KEY")
        self.openai_api_base = self._get("OPENAI_API_BASE")
        self.openai_model = self._get("OPENAI_MODEL")
        self.gmail_password = self._get("GMAIL_PASSWORD")
        self.huggingface_api_key = self._get("HUGGINGFACE_API_KEY")
        self.llama_model_name = self._get("LLAMA_MODEL_NAME")
        self.search_engine = self._get("SEARCH_ENGINE", SearchEngineType.SERPAPI_GOOGLE)
        self.web_browser_engine = WebBrowserEngineType(
            self._get("WEB_BROWSER_ENGINE", WebBrowserEngineType.PLAYWRIGHT)
        )
        self.selenium_browser_type = self._get("SELENIUM_BROWSER_TYPE", "chrome")
        self.long_term_memory = self._get("LONG_TERM_MEMORY", False)
        if self.long_term_memory:
            logger.warning("LONG TERM MEMORY is True")
        self.max_budget = self._get("MAX_BUDGET", 10.0)
        self.max_quota_seeding = self._get("MAX_QUOTA_SEEDING", 10)
        self.total_seeding = 0
        self.total_cost = 0.0
        self.update_costs = self._get("UPDATE_COSTS", True)
        self.calc_usage = self._get("CALC_USAGE", True)
        self.rpm = self._get("RPM", 10)
        self.model_for_researcher_summary = self._get("MODEL_FOR_RESEARCHER_SUMMARY")
        self.model_for_researcher_report = self._get("MODEL_FOR_RESEARCHER_REPORT")

CONFIG = Config()