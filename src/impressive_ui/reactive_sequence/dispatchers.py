from functools import singledispatch


@singledispatch
def insert_widget(container, widget, index: int) -> None:
    """Insert widget at specific index."""
    container_t = type(container).__name__
    raise NotImplementedError(
        f"""
        insert_widget not implemented for {container_t}
        If you need this functionality, please define how to insert a widget into {container_t}.

        @insert_widget.register
        def _(container: {container_t}, widget: YourWidgetType, index: int) -> None:
            ...
        """
    )


@singledispatch
def remove_widget(container, widget) -> None:
    """Remove widget from container."""
    container_t = type(container).__name__
    raise NotImplementedError(
        f"""
        remove_widget not implemented for {container_t}
        If you need this functionality, please define how to remove a widget from {container_t}.

        @remove_widget.register
        def _(container: {container_t}, widget: YourWidgetType) -> None:
            ...
        """
    )
