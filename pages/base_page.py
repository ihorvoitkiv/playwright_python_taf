import logging
import typing
from contextlib import contextmanager
from typing import Callable

import allure
from playwright.async_api import Route
from playwright.sync_api import Page, Response, Dialog, ConsoleMessage

logger = logging.getLogger(__name__)


class BasePage:

    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.page.on('console', self._console_error_handler)

    def open(self, url: str, **kwargs) -> Response | None:
        with allure.step(f'Open url: "{url}"'):
            return self.page.goto(url, wait_until='networkidle', **kwargs)

    def reload(self, **kwargs) -> Response | None:
        with allure.step(f'Reload page url: "{self.page.url}"'):
            return self.page.reload(wait_until='domcontentloaded', **kwargs)

    def scroll_by(self, x: float = 0, y: float = 0):
        with allure.step(f'Scroll by x: {x}, y: {y} coordinates'):
            self.page.mouse.wheel(delta_x=x, delta_y=y)

    def _console_error_handler(self, message: ConsoleMessage) -> None:
        if message.type == 'error':
            logger.error(f'page: {self.page.url}, console error: {message.text}')

    def _dialog_handler(self, dialog: Dialog, **kwargs) -> None:
        logger.warning(f'page: {self.page.url}, dialog text: {dialog.message}')
        dialog.accept(**kwargs)

    @allure.step
    @contextmanager
    def intercept_requests(self, url: str, payload: str, status_code: int = 200, **kwargs) -> Callable:
        def handler(route: Route) -> None:
            route.fulfill(status=status_code, body=payload)

        self.page.route(url, handler, **kwargs)
        yield
        self.page.unroute(url)

    def execute_js(self, js: str) -> typing.Any:
        return self.page.evaluate(js)

    @allure.step
    def take_screenshot(self, **kwargs) -> bytes:
        return self.page.screenshot(**kwargs)
