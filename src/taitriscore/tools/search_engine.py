from __future__ import annotations

import json

from taitriscore.config import CONFIG
from taitriscore.logs import logger
from taitriscore.tools import SearchEngineType
from taitriscore.tools.search_engine_serpapi import SerpAPIWrapper


class SearchEngine:
    def __init__(self, engine=None, run_func=None):
        self.config = CONFIG
        self.run_func = run_func
        self.engine = engine or self.config.search_engine

    # Asynchronous function to run a search query
    async def run(self, query: str, max_results=8):
        if self.engine == SearchEngineType.SERPAPI_GOOGLE:
            search = SerpAPIWrapper(serpapi_api_key=self.config.serpapi_api_key)
            rsp = await search.run(query)
        else:
            raise NotImplementedError
        return rsp


if __name__ == "__main__":
    # Example usage of the SearchEngine class
    SearchEngine.run(query="some query")