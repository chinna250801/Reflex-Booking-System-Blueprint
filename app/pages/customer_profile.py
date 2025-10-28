import reflex as rx
from app.states.management_state import ManagementState


def customer_profile_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Customer Profile", class_name="text-2xl font-bold text-gray-900 mb-6"
        ),
        rx.el.div(
            rx.el.p("Customer profile page content will be here."),
            class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
        ),
        class_name="max-w-[1200px] w-full mx-auto",
    )