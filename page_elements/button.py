import allure
from playwright.sync_api import expect

from page_elements.base_element import Element


class Button(Element):
    @property
    def type_of(self) -> str:
        return self.__class__.__name__

    def hover(self, **kwargs) :
        with allure.step(f'Hover on "{self.name}" {self.type_of}'):
            self.locator_obj.hover(**kwargs)
            return self

    def dbl_click(self, **kwargs):
        with allure.step(f'Double click on "{self.name}" {self.type_of}'):
            self.locator_obj.dblclick(**kwargs)
            return self

    def assert_element_enabled(self, **kwargs):
        with allure.step(f'Verify that "{self.name}" {self.type_of} is enabled'):
            expect(self.locator_obj).to_be_enabled(**kwargs)
