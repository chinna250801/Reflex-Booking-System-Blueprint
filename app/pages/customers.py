import reflex as rx
from app.states.management_state import ManagementState
from app.models import Customer


def customer_card(customer: Customer) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={customer['full_name']}",
                    class_name="h-12 w-12 rounded-full",
                ),
                rx.el.div(
                    rx.el.h3(
                        customer["full_name"], class_name="font-semibold text-gray-800"
                    ),
                    rx.el.p(customer["mobile"], class_name="text-sm text-gray-600"),
                ),
                class_name="flex items-center gap-4",
            ),
            rx.el.button(
                "View Profile",
                class_name="px-4 py-1.5 text-sm border rounded-md hover:bg-gray-50",
            ),
            class_name="flex justify-between items-center",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("mail", class_name="h-4 w-4 text-gray-500"),
                rx.el.span(customer["email"], class_name="text-sm text-gray-600"),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.icon("map-pin", class_name="h-4 w-4 text-gray-500"),
                rx.el.span(customer["location"], class_name="text-sm text-gray-600"),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center gap-6 mt-4 pt-4 border-t",
        ),
        class_name="p-4 bg-white rounded-xl border border-gray-200 shadow-sm",
    )


def customers_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Customers", class_name="text-2xl font-bold text-gray-900 mb-6"),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                ),
                rx.el.input(
                    placeholder="Search customers by name or mobile...",
                    on_change=ManagementState.set_customer_search_term,
                    class_name="w-full pl-10 pr-4 py-2 border rounded-lg",
                ),
                class_name="relative w-full max-w-md",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.foreach(ManagementState.filtered_customers, customer_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        class_name="max-w-[1200px] w-full mx-auto",
        on_mount=ManagementState.on_management_load,
    )