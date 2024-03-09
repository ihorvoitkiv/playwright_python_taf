import allure
from playwright.sync_api import expect

from page_elements.base_element import Element


class Input(Element):
    @property
    def type_of(self) -> str:
        return self.__class__.__name__

    def fill_in(self, value: str, validate_value=False):
        with allure.step(f'Fill in "{self.name}" {self.type_of} with value: "{value}"'):
            self.locator_obj.fill(value)

            if validate_value:
                with allure.step(f'Verify that "{self.name}" {self.type_of} has value: "{value}"'):
                    expect(self.locator_obj).to_have_value(value)

    def clear(self, **kwargs):
        with allure.step(f'Clear on "{self.name}" {self.type_of}'):
            self.locator_obj.clear(**kwargs)
            return self
