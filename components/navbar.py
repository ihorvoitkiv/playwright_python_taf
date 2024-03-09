from playwright.sync_api import Page

from components.search_modal import SearchModal
from page_elements.button import Button
from page_elements.link import Link
from pages.base_page import BasePage

from utils.enum.js_snippets import JsSnippets


class Navbar(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.search_modal = SearchModal(page)

        self.api_link = Link(page, selector="//a[text()='API']", name='API')
        self.docs_link = Link(page, selector="//a[text()='Docs']", name='Docs')
        self.theme_button = Button(page, selector=".clean-btn.toggleButton_gllP", name='Theme mode button')
        self.search_button = Button(page, selector="button.DocSearch-Button", name='Search')

    def open_docs(self):
        self.docs_link.click()

    def open_api(self):
        self.api_link.click()

    def change_theme(self):
        self.theme_button.click()

    def open_search(self):
        self.search_button.assert_element_visible()

        self.search_button.hover().click()
        self.search_modal.assert_opened()

    def _get_theme_mode(self):
        return self.execute_js(JsSnippets.THEME_MODE.value)

    def assert_theme_mode(self, expected_theme: str):
        assert self._get_theme_mode() == expected_theme
