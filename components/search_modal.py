from playwright.sync_api import Page

from page_elements.input import Input
from page_elements.list_item import ListItem
from page_elements.title import Title
from pages.base_page import BasePage


class SearchModal(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.empty_results_title = Title(page, selector='p.DocSearch-Help', name='Empty results')
        self.search_input = Input(page, selector='#docsearch-input', name='Search docs')
        self.search_result = ListItem(page, selector='#docsearch-item-{result_number}', name='Result item')

    def assert_opened(self):
        self.search_input.assert_element_visible()
        self.empty_results_title.assert_element_visible()

    def find_result(self, keyword: str, result_number: int) -> None:
        self.search_input.fill_in(keyword, validate_value=True)
        self.search_result.format_selector(result_number=result_number).click()
