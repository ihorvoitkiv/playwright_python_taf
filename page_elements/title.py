from page_elements.base_element import Element


class Title(Element):

    @property
    def type_of(self) -> str:
        return self.__class__.__name__
