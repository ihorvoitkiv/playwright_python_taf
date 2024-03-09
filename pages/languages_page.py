from playwright.sync_api import Page

from components.navbar import Navbar
from page_elements.title import Title
from pages.base_page import BasePage


class LanguagesPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.navbar = Navbar(self.page)

        self.language_title = Title(page, selector='h2#{language}', name='Language title')

    def assert_language_title_present(self, language: str):
        self.language_title.format_selector(language=language).assert_element_visible()

