from typing import TypedDict
from typing_extensions import Unpack
from PySide6.QtWidgets import QWidget


class StyleDict(TypedDict, total=False):
    accent_color: str
    alternate_background_color: str
    background: str
    background_color: str
    border: str
    border_color: str
    border_radius: str
    border_style: str
    border_width: str
    color: str
    font: str
    font_family: str
    font_size: str
    font_style: str
    font_weight: str
    height: str
    margin: str
    margin_bottom: str
    margin_left: str
    margin_right: str
    margin_top: str
    max_height: str
    max_width: str
    min_height: str
    min_width: str
    padding: str
    padding_bottom: str
    padding_left: str
    padding_right: str
    padding_top: str
    text_align: str
    text_decoration: str
    width: str


class Style:
    def __init__(self, selector: str = "", **styles: Unpack[StyleDict]) -> None:
        self.selector = selector
        self.styles = styles

    def with_selector(self, selector: str) -> "Style":
        """Set the selector for this style."""
        new_style = Style(selector, **self.styles)
        return new_style

    def compile(self) -> str:
        """Compile the styles into a CSS string."""
        if not self.styles:
            return ""

        # Convert Python-style property names to CSS-style
        css_properties = []
        for key, value in self.styles.items():
            css_key = key.replace("_", "-")
            css_properties.append(f"    {css_key}: {value};")

        css_body = "\n".join(css_properties)

        if self.selector:
            return f"{self.selector} {{\n{css_body}\n}}"
        else:
            return css_body

    @classmethod
    def __class_getitem__(
        cls, selectors: type[QWidget] | tuple[type[QWidget], ...] | str
    ) -> type["Style"]:
        """Allow Style to be used as a generic type."""
        match selectors:
            case str():
                selector = selectors
            case type() as widget_type:
                selector = widget_type.__name__
            case tuple() as widget_types:
                selector = ", ".join(widget_type.__name__ for widget_type in widget_types)
            case _:
                raise TypeError(f"Unsupported selector type: {selectors}")
        
        class _SelectorStyle(Style):
            def __init__(self, **styles: Unpack[StyleDict]) -> None:
                super().__init__(selector, **styles)
        
        return _SelectorStyle
