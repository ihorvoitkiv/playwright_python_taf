from enum import Enum
from playwright.sync_api import Playwright, BrowserType
import pytest


class BrowserTypeEnum(Enum):
    CHROMIUM = 'chromium'
    FIREFOX = 'firefox'
    WEBKIT = 'webkit'


class BrowserFactory:
    @staticmethod
    def get_instance(playwright: Playwright, name: str | BrowserTypeEnum) -> BrowserType:
        """Get a Playwright browser instance based on the given browser type.

        Args:
            playwright: The Playwright instance.
            name: The name of the browser type.
        """
        try:
            return getattr(playwright, name.value if isinstance(name, BrowserTypeEnum) else name.lower())
        except AttributeError as e:
            raise pytest.UsageError(f'Unsupported browser type: "{name}": {e}. '
                                    f'Please choose one of: {", ".join(browser.value for browser in BrowserTypeEnum)}.')
