import reflex as rx
from app.states.appointments_state import AppointmentsState
from app.models import Appointment


def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Pending",
                "px-2 py-0.5 text-xs font-medium text-yellow-800 bg-yellow-100 rounded-full",
            ),
            (
                "Confirmed",
                "px-2 py-0.5 text-xs font-medium text-blue-800 bg-blue-100 rounded-full",
            ),
            (
                "Completed",
                "px-2 py-0.5 text-xs font-medium text-emerald-800 bg-emerald-100 rounded-full",
            ),
            (
                "Cancelled",
                "px-2 py-0.5 text-xs font-medium text-red-800 bg-red-100 rounded-full",
            ),
            (
                "No-Show",
                "px-2 py-0.5 text-xs font-medium text-gray-800 bg-gray-200 rounded-full",
            ),
            "px-2 py-0.5 text-xs font-medium text-gray-800 bg-gray-100 rounded-full",
        ),
    )


def appointment_card(appointment: Appointment) -> rx.Component:
    """A card displaying a single appointment's information."""
    customer_name = AppointmentsState.customer_details.get(
        appointment["customer_id"], {}
    ).get("name", "N/A")
    customer_avatar = AppointmentsState.customer_details.get(
        appointment["customer_id"], {}
    ).get("avatar", "")
    provider_name = AppointmentsState.provider_details.get(
        appointment["provider_id"], "N/A"
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.image(src=customer_avatar, class_name="h-10 w-10 rounded-full"),
                rx.el.div(
                    rx.el.h3(customer_name, class_name="font-semibold text-gray-800"),
                    rx.el.p(
                        f"with {provider_name}", class_name="text-sm text-gray-600"
                    ),
                ),
                class_name="flex items-center gap-3",
            ),
            status_badge(appointment["status"]),
            class_name="flex justify-between items-center pb-3 border-b",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("calendar", class_name="h-4 w-4 text-gray-500"),
                rx.el.span(
                    AppointmentsState.appointment_datetimes[appointment["id"]]["date"],
                    class_name="text-sm text-gray-600",
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.icon("clock", class_name="h-4 w-4 text-gray-500"),
                rx.el.span(
                    AppointmentsState.appointment_datetimes[appointment["id"]]["time"],
                    class_name="text-sm text-gray-600",
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.icon("dollar-sign", class_name="h-4 w-4 text-gray-500"),
                rx.el.span(
                    AppointmentsState.appointment_prices[appointment["id"]],
                    class_name="text-sm text-gray-600",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center gap-6 mt-3",
        ),
        rx.cond(
            ~(
                (appointment["status"] == "Completed")
                | (appointment["status"] == "Cancelled")
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.button(
                        "Confirm",
                        on_click=lambda: AppointmentsState.update_status(
                            appointment["id"], "Confirmed"
                        ),
                        class_name="text-sm px-3 py-1 border rounded-md hover:bg-gray-50",
                    ),
                    rx.el.button(
                        "Complete",
                        on_click=lambda: AppointmentsState.update_status(
                            appointment["id"], "Completed"
                        ),
                        class_name="text-sm px-3 py-1 border rounded-md hover:bg-gray-50",
                    ),
                    rx.el.button(
                        "No-Show",
                        on_click=lambda: AppointmentsState.update_status(
                            appointment["id"], "No-Show"
                        ),
                        class_name="text-sm px-3 py-1 border rounded-md hover:bg-gray-50",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.div(
                    rx.el.button(
                        "Edit Time",
                        class_name="text-sm px-3 py-1 border rounded-md hover:bg-gray-50",
                    ),
                    rx.el.button(
                        "Cancel",
                        on_click=lambda: AppointmentsState.update_status(
                            appointment["id"], "Cancelled"
                        ),
                        class_name="text-sm px-3 py-1 border rounded-md text-red-600 hover:bg-red-50",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="flex justify-between items-center mt-4 pt-4 border-t",
            ),
            None,
        ),
        class_name="p-4 bg-white rounded-xl border border-gray-200 shadow-sm flex flex-col",
    )


def filter_controls() -> rx.Component:
    """The filter controls for the appointments page."""
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search",
                class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
            ),
            rx.el.input(
                placeholder="Search by customer name...",
                on_change=AppointmentsState.set_search_term,
                class_name="w-full max-w-sm pl-10 pr-4 py-2 border rounded-lg",
                debounce_timeout=300,
            ),
            class_name="relative",
        ),
        rx.el.select(
            rx.el.option("All Statuses", value="all"),
            rx.foreach(
                AppointmentsState.status_options,
                lambda status: rx.el.option(status, value=status),
            ),
            value=AppointmentsState.status_filter,
            on_change=AppointmentsState.set_status_filter,
            class_name="py-2 px-4 border rounded-lg bg-white shadow-sm",
        ),
        class_name="flex items-center justify-between mb-6",
    )


def appointments_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Appointments", class_name="text-2xl font-bold text-gray-900 mb-6"),
        filter_controls(),
        rx.cond(
            AppointmentsState.filtered_appointments.length() > 0,
            rx.el.div(
                rx.foreach(AppointmentsState.filtered_appointments, appointment_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
            ),
            rx.el.div(
                rx.el.p("No appointments found for the selected filters."),
                class_name="text-center py-12 text-gray-500 bg-gray-50 rounded-lg",
            ),
        ),
        class_name="max-w-[1600px] w-full mx-auto",
        on_mount=AppointmentsState.on_load,
    )