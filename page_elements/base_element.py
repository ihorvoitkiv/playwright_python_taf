from abc import ABC, abstractmethod
import allure
from playwright.sync_api import Locator, Page, expect


class Element(ABC):
    """Abstract class for basic and complex HTML elements initialization, for further interaction on web pages"""

    def __init__(self, page: Page, selector: str, name: str) -> None:
        """
        Initializes an Element object.

        Args:
            page (Page): The Playwright page instance.
            name (str): The element identifier
            selector (str): The element selector
        """
        self.page = page
        self.name = name
        self.selector = selector

    @property
    @abstractmethod
    def type_of(self) -> str:
        """Returns the element type (Title, Link, Button, etc.)"""
        pass

    @property
    def locator_obj(self) -> Locator:
        """Returns the element using playwright Locator object, used for actions"""
        return self.page.locator(self.selector)

    def format_selector(self, *args, **kwargs) -> 'Element':
        """Formats init selector string with provided key-value pairs arguments"""
        self.selector = self.selector.format(*args, **kwargs)
        return self

    def click(self, **kwargs) -> 'Element':
        with allure.step(f'Click on "{self.name}" {self.type_of}'):
            self.locator_obj.click(**kwargs)
            return self

    def scroll_to_element(self, **kwargs) -> 'Element':
        with allure.step(f'Scroll to "{self.name}" {self.type_of}'):
            self.locator_obj.scroll_into_view_if_needed(**kwargs)
            return self

    def assert_element_visible(self, **kwargs):
        with allure.step(f'Verify that "{self.name}" {self.type_of} is visible'):
            expect(self.locator_obj).to_be_visible(**kwargs)

    def assert_element_not_visible(self, **kwargs):
        with allure.step(f'Verify that "{self.name}" {self.type_of} is not visible'):
            expect(self.locator_obj).not_to_be_visible(**kwargs)
