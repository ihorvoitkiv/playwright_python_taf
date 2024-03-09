import pytest
from playwright.sync_api import Page

from pages.languages_page import LanguagesPage
from pages.main_page import MainPage


@pytest.fixture(scope='function')
def main_page(page: Page) -> MainPage:
    return MainPage(page)


@pytest.fixture(scope='function')
def languages_page(page: Page) -> LanguagesPage:
    return LanguagesPage(page)
