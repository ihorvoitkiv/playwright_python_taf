from playwright.sync_api import Page

from components.navbar import Navbar
from pages.base_page import BasePage


class MainPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.navbar = Navbar(self.page)
