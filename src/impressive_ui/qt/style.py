from dataclasses import dataclass
from typing import TypedDict
from typing_extensions import Unpack
from PySide6.QtWidgets import QWidget


class StyleDict(TypedDict, total=False):
    accent_color: str
    alternate_background_color: str
    background: str
    background_color: str
    background_image: str
    background_repeat: str
    background_position: str
    background_attachment: str
    background_clip: str
    background_origin: str
    border: str
    border_top: str
    border_right: str
    border_bottom: str
    border_left: str
    border_color: str
    border_top_color: str
    border_right_color: str
    border_bottom_color: str
    border_left_color: str
    border_image: str
    border_radius: str
    border_top_left_radius: str
    border_top_right_radius: str
    border_bottom_right_radius: str
    border_bottom_left_radius: str
    border_style: str
    border_top_style: str
    border_right_style: str
    border_bottom_style: str
    border_left_style: str
    border_width: str
    border_top_width: str
    border_right_width: str
    border_bottom_width: str
    border_left_width: str
    bottom: str
    button_layout: str
    color: str
    dialogbuttonbox_buttons_have_icons: str
    font: str
    font_family: str
    font_size: str
    font_style: str
    font_weight: str
    gridline_color: str
    height: str
    icon: str
    icon_size: str
    image: str
    image_position: str
    left: str
    letter_spacing: str
    lineedit_password_character: str
    lineedit_password_mask_delay: str
    margin: str
    margin_bottom: str
    margin_left: str
    margin_right: str
    margin_top: str
    max_height: str
    max_width: str
    messagebox_text_interaction_flags: str
    min_height: str
    min_width: str
    opacity: str
    outline: str
    outline_color: str
    outline_offset: str
    outline_style: str
    outline_radius: str
    outline_bottom_left_radius: str
    outline_bottom_right_radius: str
    outline_top_left_radius: str
    outline_top_right_radius: str
    padding: str
    padding_bottom: str
    padding_left: str
    padding_right: str
    padding_top: str
    paint_alternating_row_colors_for_empty_area: str
    placeholder_text_color: str
    position: str
    right: str
    selection_background_color: str
    selection_color: str
    show_decoration_selected: str
    spacing: str
    subcontrol_origin: str
    subcontrol_position: str
    titlebar_show_tooltips_on_buttons: str
    widget_animation_duration: str
    text_align: str
    text_decoration: str
    top: str
    width: str
    word_spacing: str
    _qt_background_role: str
    _qt_style_features: str


@dataclass
class QtStyleSheet:
    selector: str
    styles: StyleDict

    def compile(self) -> str:
        """Compile the styles into a CSS string."""
        if not self.styles:
            return ""
        css_body = "\n".join(
            f"    {key.replace('_', '-')}: {value};"
            for key, value in self.styles.items()
        )

        if self.selector:
            return f"{self.selector} {{\n{css_body}\n}}\n"
        else:
            return f"{{\n{css_body}\n}}\n"


class qss:
    """Utility class for easily creating Qt stylesheets."""

    def __new__(cls, **styles: Unpack[StyleDict]) -> str:
        """Create a new Style instance with the given styles."""
        return QtStyleSheet(selector="", styles=styles).compile()

    def __class_getitem__(
        cls, selectors: type[QWidget] | tuple[type[QWidget], ...] | str
    ) -> type["qss"]:
        """Allow Style to be used as a generic type."""
        match selectors:
            case str():
                selector = selectors
            case type() as widget_type:
                selector = widget_type.__name__
            case tuple() as widget_types:
                selector = ", ".join(
                    widget_type.__name__ for widget_type in widget_types
                )
            case _:
                raise TypeError(f"Unsupported selector type: {selectors}")

        class _SelectorStyle(qss):
            def __new__(cls, **styles: Unpack[StyleDict]) -> str:
                """Create a new Style instance with the given styles and selector."""
                return QtStyleSheet(selector=selector, styles=styles).compile()

        return _SelectorStyle
