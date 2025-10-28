import reflex as rx
from app.states.management_state import ManagementState
from app.models import Provider, Department


def provider_form_modal() -> rx.Component:
    """A modal for adding or editing a provider."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4"),
                "Add Provider",
                on_click=lambda: ManagementState.open_provider_modal(),
                class_name="flex items-center gap-2 bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 transition-colors",
            )
        ),
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    ManagementState.provider_form_is_edit,
                    "Edit Provider",
                    "Add New Provider",
                ),
                class_name="text-lg font-semibold",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.label("Full Name", class_name="text-sm font-medium"),
                        rx.el.input(
                            placeholder="e.g., Dr. Jane Doe",
                            name="name",
                            class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500",
                            default_value=ManagementState.provider_name,
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Departments", class_name="text-sm font-medium"),
                        rx.el.div(
                            rx.foreach(
                                ManagementState.departments,
                                lambda dept: rx.el.div(
                                    rx.el.input(
                                        type="checkbox",
                                        checked=ManagementState.provider_department_ids.contains(
                                            dept.id
                                        ),
                                        on_change=lambda checked: ManagementState.toggle_provider_department(
                                            dept.id, checked
                                        ),
                                        class_name="h-4 w-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500",
                                    ),
                                    rx.el.label(
                                        dept.name,
                                        class_name="ml-2 text-sm text-gray-700",
                                    ),
                                    class_name="flex items-center",
                                ),
                            ),
                            class_name="grid grid-cols-2 gap-2 mt-2",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Bio", class_name="text-sm font-medium"),
                        rx.el.textarea(
                            placeholder="A short bio about the provider.",
                            name="bio",
                            class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500",
                            default_value=ManagementState.provider_bio,
                        ),
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Contact Mobile", class_name="text-sm font-medium"
                            ),
                            rx.el.input(
                                placeholder="555-0101",
                                name="contact_mobile",
                                class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500",
                                default_value=ManagementState.provider_contact_mobile,
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Contact Email", class_name="text-sm font-medium"
                            ),
                            rx.el.input(
                                type="email",
                                name="contact_email",
                                placeholder="jane.d@example.com",
                                class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500",
                                default_value=ManagementState.provider_contact_email,
                            ),
                            class_name="flex-1",
                        ),
                        class_name="flex gap-4",
                    ),
                    rx.el.div(
                        rx.el.label("Status", class_name="text-sm font-medium"),
                        rx.el.select(
                            rx.el.option("Active", value="Active"),
                            rx.el.option("Inactive", value="Inactive"),
                            value=ManagementState.provider_status,
                            on_change=ManagementState.set_provider_status,
                            class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500",
                            disabled=~ManagementState.provider_form_is_edit,
                        ),
                    ),
                    rx.cond(
                        ManagementState.provider_error != "",
                        rx.el.p(
                            ManagementState.provider_error,
                            class_name="text-sm text-red-600 mt-1",
                        ),
                        None,
                    ),
                    class_name="space-y-4",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            on_click=ManagementState.close_provider_modal,
                            class_name="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300",
                            type="button",
                        )
                    ),
                    rx.el.button(
                        rx.cond(
                            ManagementState.provider_form_is_edit,
                            "Save Changes",
                            "Add Provider",
                        ),
                        type="submit",
                        class_name="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700",
                    ),
                    class_name="flex justify-end gap-3 mt-6",
                ),
                class_name="mt-4",
                on_submit=ManagementState.save_provider,
            ),
        ),
        open=ManagementState.show_provider_modal,
        on_open_change=ManagementState.set_show_provider_modal,
    )


def confirmation_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Confirm Action", class_name="text-lg font-bold"),
            rx.dialog.description(
                ManagementState.delete_warning_message, class_name="my-4 text-gray-600"
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Cancel",
                        class_name="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300",
                        type="button",
                    )
                ),
                rx.el.button(
                    "Confirm",
                    on_click=ManagementState.execute_delete,
                    class_name="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700",
                ),
                class_name="flex justify-end gap-3 mt-4",
            ),
        ),
        open=ManagementState.show_delete_confirmation,
        on_open_change=ManagementState.set_show_delete_confirmation,
    )


def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Active",
                "px-2 py-0.5 text-xs font-medium text-emerald-800 bg-emerald-100 rounded-full",
            ),
            (
                "Inactive",
                "px-2 py-0.5 text-xs font-medium text-amber-800 bg-amber-100 rounded-full",
            ),
            (
                "Archived",
                "px-2 py-0.5 text-xs font-medium text-gray-800 bg-gray-100 rounded-full",
            ),
            "px-2 py-0.5 text-xs font-medium text-gray-800 bg-gray-100 rounded-full",
        ),
    )


def provider_card(provider: Provider) -> rx.Component:
    """A card displaying a single provider's information."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3(provider.name, class_name="text-lg font-semibold text-gray-800"),
            status_badge(provider.status),
            class_name="flex justify-between items-center",
        ),
        rx.el.p(
            ManagementState.provider_department_names[provider.id],
            class_name="text-sm font-medium text-emerald-700 mt-1",
        ),
        rx.el.p(provider.bio, class_name="text-sm text-gray-600 mt-2 truncate"),
        rx.el.div(
            rx.el.div(
                rx.icon("phone", class_name="h-4 w-4 text-gray-500"),
                rx.el.span(provider.contact_mobile, class_name="text-sm text-gray-600"),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.icon("mail", class_name="h-4 w-4 text-gray-500"),
                rx.el.span(provider.contact_email, class_name="text-sm text-gray-600"),
                class_name="flex items-center gap-2",
            ),
            class_name="flex flex-col gap-1 mt-3",
        ),
        rx.el.div(
            rx.el.button(
                "Edit",
                on_click=lambda: ManagementState.open_provider_modal(provider),
                class_name="text-sm px-3 py-1.5 border rounded-md hover:bg-gray-50",
            ),
            rx.el.select(
                rx.el.option("Change Status", value="", disabled=True),
                rx.el.option("Active", value="Active"),
                rx.el.option("Inactive", value="Inactive"),
                value=provider.status,
                on_change=lambda new_status: ManagementState.change_provider_status(
                    provider.id, new_status
                ),
                class_name="text-sm px-3 py-1.5 border rounded-md hover:bg-gray-50 focus:outline-none focus:ring-1 focus:ring-emerald-500",
            ),
            rx.el.button(
                "Archive",
                on_click=lambda: ManagementState.confirm_archive_provider(provider.id),
                class_name="text-sm px-3 py-1.5 border rounded-md text-red-600 hover:bg-red-50",
            ),
            class_name="flex items-center gap-2 mt-4",
        ),
        class_name="p-4 bg-white rounded-xl border border-gray-200 shadow-sm flex flex-col",
    )


def providers_page() -> rx.Component:
    """The UI for the providers management page."""
    return rx.el.div(
        confirmation_dialog(),
        rx.el.div(
            rx.el.h1("Providers", class_name="text-2xl font-bold text-gray-900"),
            rx.el.div(provider_form_modal(), class_name="ml-auto"),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.foreach(ManagementState.active_providers, provider_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        class_name="max-w-[1200px] w-full mx-auto",
    )