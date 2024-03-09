from page_elements.base_element import Element


class ListItem(Element):

    @property
    def type_of(self) -> str:
        return self.__class__.__name__
