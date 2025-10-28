import reflex as rx
from app.states.calendar_state import CalendarState, FormattedSlot
from typing import Optional


def booking_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Book Appointment", class_name="text-lg font-semibold"),
            rx.dialog.description(
                "Confirm booking details for the selected slot.",
                class_name="text-sm text-gray-600",
            ),
            rx.cond(
                CalendarState.booking_slot,
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Provider:", class_name="font-medium"),
                        rx.el.p(CalendarState.selected_provider_name),
                        class_name="flex justify-between",
                    ),
                    rx.el.div(
                        rx.el.p("Date:", class_name="font-medium"),
                        rx.el.p(
                            CalendarState.booking_slot["start_datetime"]
                            .to_string()
                            .split("T")[0]
                        ),
                        class_name="flex justify-between",
                    ),
                    rx.el.div(
                        rx.el.p("Time:", class_name="font-medium"),
                        rx.el.p(
                            f"{CalendarState.booking_slot['start_datetime'].to_string().split('T')[1][:5]} - {CalendarState.booking_slot['end_datetime'].to_string().split('T')[1][:5]}"
                        ),
                        class_name="flex justify-between",
                    ),
                    rx.el.div(
                        rx.el.label("Customer", class_name="font-medium"),
                        rx.el.select(
                            rx.foreach(
                                CalendarState.customers,
                                lambda customer: rx.el.option(
                                    customer["full_name"], value=customer["id"]
                                ),
                            ),
                            value=CalendarState.booking_customer_id,
                            on_change=CalendarState.set_booking_customer_id,
                            class_name="w-full mt-1 p-2 border rounded-md",
                        ),
                        class_name="mt-4",
                    ),
                    rx.cond(
                        CalendarState.booking_error != "",
                        rx.el.p(
                            CalendarState.booking_error,
                            class_name="text-sm text-red-600 mt-2",
                        ),
                        None,
                    ),
                    class_name="mt-4 space-y-2 text-sm",
                ),
                None,
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Cancel",
                        class_name="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300",
                        on_click=CalendarState.close_booking_modal,
                    )
                ),
                rx.el.button(
                    "Confirm Booking",
                    on_click=CalendarState.confirm_booking,
                    class_name="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700",
                ),
                class_name="flex justify-end gap-3 mt-6",
            ),
        ),
        open=CalendarState.show_booking_modal,
    )


def availability_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Edit Availability", class_name="text-lg font-semibold"),
            rx.el.div(
                rx.el.p(
                    f"Editing for: {CalendarState.selected_month}",
                    class_name="text-sm text-gray-600 mb-4",
                ),
                rx.el.p(
                    "Availability editing form will be implemented in a future phase."
                ),
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Close",
                        class_name="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300",
                        on_click=CalendarState.close_availability_modal,
                    )
                ),
                class_name="flex justify-end gap-3 mt-6",
            ),
        ),
        open=CalendarState.show_availability_modal,
    )


def calendar_controls() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    CalendarState.providers,
                    lambda p: rx.el.option(p["name"], value=p["id"]),
                ),
                value=CalendarState.selected_provider_id,
                on_change=CalendarState.handle_provider_change,
                class_name="p-2 border rounded-md shadow-sm",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("chevron-left"),
                    on_click=lambda: CalendarState.change_month(-1),
                ),
                rx.el.span(
                    CalendarState.selected_month,
                    class_name="font-semibold text-lg w-28 text-center",
                ),
                rx.el.button(
                    rx.icon("chevron-right"),
                    on_click=lambda: CalendarState.change_month(1),
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex items-center gap-6",
        ),
        rx.el.button(
            "Edit Availability",
            on_click=CalendarState.open_availability_modal,
            class_name="px-4 py-2 border rounded-md text-sm",
        ),
        class_name="flex justify-between items-center mb-6",
    )


def slot_chip(slot: FormattedSlot) -> rx.Component:
    return rx.el.div(
        rx.el.span(slot["time_str"]),
        on_click=rx.cond(
            slot["is_booked"], rx.noop(), CalendarState.open_booking_modal(slot)
        ),
        class_name=rx.cond(
            slot["is_booked"],
            "px-1.5 py-0.5 text-xs text-gray-600 bg-gray-200 rounded-md cursor-not-allowed w-fit",
            "px-1.5 py-0.5 text-xs text-emerald-800 bg-emerald-100 rounded-md cursor-pointer hover:bg-emerald-200 w-fit",
        ),
    )


def day_cell(day: Optional[int]) -> rx.Component:
    day_data = CalendarState.slots_by_day.get(day, {"visible": [], "overflow": 0})
    return rx.el.div(
        rx.el.span(day, class_name="text-sm"),
        rx.el.div(
            rx.foreach(day_data["visible"], slot_chip),
            rx.cond(
                day_data["overflow"] > 0,
                rx.el.div(
                    rx.el.p(
                        f"+{day_data['overflow']} more",
                        class_name="text-xs text-gray-500 font-medium pt-1",
                    )
                ),
                None,
            ),
            class_name="flex flex-wrap gap-1 mt-1",
        ),
        class_name=rx.cond(
            day,
            "p-2 border-t border-r border-gray-200 h-32 overflow-y-auto",
            "p-2 border-t border-r border-gray-200 bg-gray-50 h-32",
        ),
    )


def calendar_grid() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.foreach(
                ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
                lambda day_name: rx.el.div(
                    day_name, class_name="p-2 text-center font-semibold text-sm"
                ),
            ),
            class_name="grid grid-cols-7 border-t border-l border-b border-gray-200 rounded-t-lg bg-gray-50",
        ),
        rx.foreach(
            CalendarState.calendar_weeks,
            lambda week: rx.el.div(
                rx.foreach(week, day_cell),
                class_name="grid grid-cols-7 border-b border-l border-gray-200",
            ),
        ),
        class_name="rounded-b-lg shadow-sm",
    )


def calendar_page() -> rx.Component:
    """The UI for the calendar page."""
    return rx.el.div(
        booking_modal(),
        availability_modal(),
        rx.el.h1("Calendar", class_name="text-2xl font-bold text-gray-900 mb-6"),
        rx.el.div(
            calendar_controls(),
            calendar_grid(),
            class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
        ),
        class_name="max-w-[1200px] w-full mx-auto",
        on_mount=CalendarState.on_calendar_load,
    )