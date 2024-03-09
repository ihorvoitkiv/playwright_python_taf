from enum import Enum


class JsSnippets(Enum):
    THEME_MODE = """
        () => {
            const htmlElement = document.querySelector('html');
            return htmlElement.getAttribute('data-theme');
        }
    """