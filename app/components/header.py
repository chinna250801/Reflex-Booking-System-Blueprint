import reflex as rx
from app.states.base_state import AppState


def header() -> rx.Component:
    """The main header component for the application."""
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon("menu", class_name="h-6 w-6"),
                    on_click=AppState.toggle_sidebar,
                    class_name="p-2 rounded-md hover:bg-gray-100 md:hidden",
                ),
                rx.icon("calendar-check", class_name="h-7 w-7 text-emerald-600"),
                rx.el.span(
                    "Appointment Manager",
                    class_name="hidden sm:block text-xl font-bold text-gray-800",
                ),
                class_name="flex items-center gap-4",
            ),
            rx.el.div(
                rx.el.p(
                    "Welcome, User", class_name="text-sm font-medium text-gray-600"
                ),
                rx.el.div(
                    rx.image(
                        src="https://api.dicebear.com/9.x/initials/svg?seed=User",
                        class_name="h-9 w-9 rounded-full",
                    ),
                    class_name="p-0.5 bg-gradient-to-tr from-emerald-500 to-cyan-500 rounded-full",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="flex items-center justify-between h-16 px-4 md:px-6",
        ),
        class_name="bg-white border-b border-gray-200 sticky top-0 z-10",
    )