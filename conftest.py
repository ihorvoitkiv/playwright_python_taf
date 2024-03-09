import logging

import allure
import pytest
from pytest import fixture, FixtureRequest
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page

from browser_factory import BrowserFactory, BrowserTypeEnum
from settings import BASE_URL


def pytest_addoption(parser) -> None:
    """
    Add custom command-line options for pytest framework

    Args:
        parser: pytest command-line option parser.
    """
    parser.addoption("--headless", action="store", default=False, help="browser headless mode: True or False")
    parser.addoption("--browser_type", action="store", default=BrowserTypeEnum.CHROMIUM,
                     help="browser type: chromium, firefox or webkit")
    parser.addoption("--url", action="store", default=BASE_URL, help="base url")


@pytest.fixture(scope="session")
def playwright() -> Playwright:
    """Pytest fixture for the Playwright instance. """
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session')
def browser(playwright: Playwright, request: FixtureRequest) -> Browser:
    """
    Pytest fixture for the browser.

    Args:
        playwright: Playwright instance.
        request: Pytest FixtureRequest object.
    """
    headless: bool = request.config.getoption('--headless')
    browser_type: str | BrowserTypeEnum = request.config.getoption('--browser_type')

    browser: Browser = BrowserFactory.get_instance(playwright=playwright, name=browser_type).launch(headless=headless)
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, tmpdir_factory: pytest.TempdirFactory) -> dict:
    """
    Pytest fixture for browser context arguments.

    Args:
        browser_context_args: Browser context arguments.
        tmpdir_factory: Pytest TempdirFactory object.
    """
    return {
        **browser_context_args,
        "record_video_dir": tmpdir_factory.mktemp('videos')
    }


@fixture(scope='function')
def browser_context(browser: Browser, browser_context_args: dict) -> BrowserContext:
    """
    Pytest fixture for browser context.

    Args:
        browser: Browser instance.
        browser_context_args: Browser context arguments.
    """
    return browser.new_context(**browser_context_args)


@pytest.fixture(scope='function')
def page(browser_context: BrowserContext) -> Page:
    """
    Pytest fixture for playwright page object.

    Args:
        browser_context: Browser context instance.
    """
    return browser_context.new_page()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item) -> None:
    """
    Pytest hook for generating test reports.

    Args:
        item: Pytest item object.
    """
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # check if test failed and attach log data
    if rep.when == "call" and rep.failed:
        try:
            page: Page | None = item.funcargs.get("page")

            allure.attach(
                page.screenshot(type='png'),
                name=f"screenshot_{item.name}.png",
                attachment_type=allure.attachment_type.PNG
            )

            video_path = page.video.path()
            page.context.close()  # ensure video saved
            allure.attach(
                open(video_path, 'rb').read(),
                name=f"video_{item.name}.webm",
                attachment_type=allure.attachment_type.WEBM
            )

        except Exception as e:
            logging.error("Failed to attach test report logs data:", e)
