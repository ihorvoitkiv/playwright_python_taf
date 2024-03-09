import pytest

from pages.main_page import MainPage
from pages.languages_page import LanguagesPage
from settings import BASE_URL


class Test:

    def test_change_theme_mode(self, main_page: MainPage):
        main_page.open(BASE_URL)

        main_page.navbar.change_theme()
        main_page.navbar.assert_theme_mode('dark')

        main_page.navbar.change_theme()
        main_page.navbar.assert_theme_mode('light')
