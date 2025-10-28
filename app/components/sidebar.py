import reflex as rx
from app.states.base_state import AppState


def nav_item(item: dict) -> rx.Component:
    """A single navigation item in the sidebar."""
    return rx.el.a(
        rx.icon(item["icon"], class_name="h-5 w-5"),
        rx.el.span(item["name"], class_name="font-medium"),
        href=item["route"],
        class_name=rx.cond(
            AppState.router.page.path == item["route"],
            "flex items-center gap-3 px-3 py-2.5 rounded-lg bg-emerald-50 text-emerald-700 transition-colors",
            "flex items-center gap-3 px-3 py-2.5 rounded-lg text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-colors",
        ),
    )


def sidebar() -> rx.Component:
    """The main sidebar component."""
    return rx.el.aside(
        rx.el.div(
            rx.el.nav(
                rx.foreach(AppState.nav_items, nav_item),
                class_name="flex flex-col gap-1.5 p-4",
            ),
            class_name="flex-1 overflow-y-auto",
        ),
        class_name="hidden md:flex flex-col w-64 border-r border-gray-200 bg-white",
    )