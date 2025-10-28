import reflex as rx
from app.states.management_state import ManagementState
from app.models import Department


def department_form_modal() -> rx.Component:
    """A modal for adding or editing a department."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4"),
                "Add Department",
                on_click=lambda: ManagementState.open_department_modal(),
                class_name="flex items-center gap-2 bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 transition-colors",
            )
        ),
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    ManagementState.department_form_is_edit,
                    "Edit Department",
                    "Add New Department",
                ),
                class_name="text-lg font-semibold",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Department Name", class_name="text-sm font-medium"
                        ),
                        rx.el.input(
                            placeholder="e.g., General Medicine",
                            name="name",
                            class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500",
                            default_value=ManagementState.department_name,
                        ),
                        class_name="space-y-1",
                    ),
                    rx.el.div(
                        rx.el.label("Description", class_name="text-sm font-medium"),
                        rx.el.textarea(
                            placeholder="Brief description of the department's services.",
                            name="description",
                            class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500",
                            default_value=ManagementState.department_description,
                        ),
                        class_name="space-y-1",
                    ),
                    rx.cond(
                        ManagementState.department_error != "",
                        rx.el.p(
                            ManagementState.department_error,
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
                            on_click=ManagementState.close_department_modal,
                            class_name="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300",
                            type="button",
                        )
                    ),
                    rx.el.button(
                        rx.cond(
                            ManagementState.department_form_is_edit,
                            "Save Changes",
                            "Add Department",
                        ),
                        type="submit",
                        class_name="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700",
                    ),
                    class_name="flex justify-end gap-3 mt-6",
                ),
                class_name="mt-4",
                on_submit=ManagementState.save_department,
            ),
        ),
        open=ManagementState.show_department_modal,
        on_open_change=ManagementState.set_show_department_modal,
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


def department_card(department: Department) -> rx.Component:
    """A card displaying a single department's information."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                department["name"], class_name="text-lg font-semibold text-gray-800"
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="h-4 w-4"),
                    on_click=lambda: ManagementState.open_department_modal(department),
                    class_name="p-2 text-gray-500 hover:text-emerald-600 hover:bg-emerald-50 rounded-md",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: ManagementState.confirm_delete_department(
                        department["id"]
                    ),
                    class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex justify-between items-center",
        ),
        rx.el.p(department["description"], class_name="text-sm text-gray-600 mt-2"),
        class_name="p-4 bg-white rounded-xl border border-gray-200 shadow-sm",
    )


def departments_page() -> rx.Component:
    """The UI for the departments management page."""
    return rx.el.div(
        confirmation_dialog(),
        rx.el.div(
            rx.el.h1("Departments", class_name="text-2xl font-bold text-gray-900"),
            rx.el.div(department_form_modal(), class_name="ml-auto"),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.foreach(ManagementState.departments, department_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        class_name="max-w-[1200px] w-full mx-auto",
    )