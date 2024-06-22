from __future__ import annotations

import importlib
from typing import Callable

from typing_extensions import Any, Coroutine, Literal, overload

from taitriscore.config import CONFIG
from taitriscore.tools import SearchEngineType, WebBrowserEngineType
from taitriscore.utils.parse_html import WebPage


class WebBrowserEngine:
    def __init__(
        self,
        engine: WebBrowserEngineType | None = None,
        run_func: (
            Callable[..., Coroutine[Any, Any, WebPage | list[WebPage]]] | None
        ) = None,
    ):
        engine = engine or CONFIG.web_browser_engine

        if engine == WebBrowserEngineType.SELENIUM:
            module = "taitriscore.tools.web_browser_engine_selenium"
            run_func = importlib.import_module(module).SeleniumWrapper().run
        elif engine == WebBrowserEngineType.CUSTOM:
            run_func = run_func
        else:
            raise NotImplementedError
        self.run_func = run_func
        self.engine = engine

    @overload
    async def run(self, url: str) -> WebPage: ...

    @overload
    async def run(self, url: str, *urls: str) -> list[WebPage]: ...

    # Asynchronous function to run a web browser engine
    async def run(self, url: str, *urls: str) -> WebPage | list[WebPage]:
        return await self.run_func(url, *urls)


if __name__ == "__main__":
    import fire

    # Main function to execute WebBrowserEngine with fire CLI
    async def main(
        url: str,
        *urls: str,
        engine_type: Literal["playwright", "selenium"] = "playwright",
        **kwargs,
    ):
        return await WebBrowserEngine(WebBrowserEngineType(engine_type), **kwargs).run(
            url, *urls
        )

    fire.Fire(main)