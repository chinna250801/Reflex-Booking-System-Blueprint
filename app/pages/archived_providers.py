import reflex as rx
from app.states.management_state import ManagementState
from app.models import Provider
from app.pages.providers import status_badge


def archived_provider_card(provider: Provider) -> rx.Component:
    """A card displaying an archived provider's information."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                provider["name"], class_name="text-lg font-semibold text-gray-800"
            ),
            status_badge(provider["status"]),
            class_name="flex justify-between items-center",
        ),
        rx.el.p(
            ManagementState.provider_department_names.get(provider["id"], "N/A"),
            class_name="text-sm font-medium text-gray-600 mt-1",
        ),
        rx.el.p(provider["bio"], class_name="text-sm text-gray-500 mt-2 truncate"),
        rx.el.div(
            rx.el.div(
                rx.icon("phone", class_name="h-4 w-4 text-gray-500"),
                rx.el.span(
                    provider["contact_mobile"], class_name="text-sm text-gray-600"
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.icon("mail", class_name="h-4 w-4 text-gray-500"),
                rx.el.span(
                    provider["contact_email"], class_name="text-sm text-gray-600"
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex flex-col gap-1 mt-3",
        ),
        rx.el.div(
            rx.el.button(
                "Restore",
                on_click=lambda: ManagementState.restore_provider(provider["id"]),
                class_name="text-sm px-3 py-1.5 border rounded-md text-emerald-600 hover:bg-emerald-50",
            ),
            class_name="flex items-center gap-2 mt-4",
        ),
        class_name="p-4 bg-white rounded-xl border border-gray-200 shadow-sm flex flex-col",
    )


def archived_providers_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Archived Providers", class_name="text-2xl font-bold text-gray-900 mb-6"
        ),
        rx.el.div(
            rx.cond(
                ManagementState.archived_providers.length() > 0,
                rx.el.div(
                    rx.foreach(
                        ManagementState.archived_providers, archived_provider_card
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                rx.el.div(
                    rx.el.p("There are no archived providers."),
                    class_name="text-center py-12 text-gray-500",
                ),
            )
        ),
        class_name="max-w-[1200px] w-full mx-auto",
    )