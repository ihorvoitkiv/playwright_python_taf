import allure
from playwright.sync_api import expect

from page_elements.base_element import Element


class CheckBox(Element):

    @property
    def type_of(self) -> str:
        return self.__class__.__name__

    def check(self, **kwargs):
        with allure.step(f'Check on "{self.name}" {self.type_of}'):
            self.locator_obj.check(**kwargs)
            return self

    def uncheck(self, **kwargs):
        with allure.step(f'Uncheck on "{self.name}" {self.type_of}'):
            self.locator_obj.uncheck(**kwargs)
            return self

    def assert_element_checked(self, **kwargs):
        with allure.step(f'Verify that "{self.name}" {self.type_of} is checked'):
            expect(self.locator_obj).to_be_checked(**kwargs)

    def assert_element_not_checked(self, **kwargs):
        with allure.step(f'Verify that "{self.name}" {self.type_of} is not checked'):
            expect(self.locator_obj).not_to_be_checked(**kwargs)
