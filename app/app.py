import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.states.base_state import AppState
from app.pages import (
    dashboard,
    calendar,
    appointments,
    customers,
    providers,
    departments,
    business_settings,
    reports,
    archived_providers,
    customer_profile,
)
from app.db import create_db_and_tables, seed_database


def page_layout(page_content: rx.Component) -> rx.Component:
    """The main layout for all pages."""
    return rx.el.div(
        header(),
        rx.el.div(
            sidebar(),
            rx.el.main(
                page_content, class_name="flex-1 p-4 md:p-6 lg:p-8 overflow-y-auto"
            ),
            class_name="flex min-h-screen",
        ),
        class_name="font-['Roboto'] bg-gray-50 text-gray-800",
    )


def index() -> rx.Component:
    return page_layout(dashboard.dashboard_page())


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", title="Dashboard | Appointment Manager")
app.add_page(
    lambda: page_layout(calendar.calendar_page()),
    route="/calendar",
    title="Calendar | Appointment Manager",
)
app.add_page(
    lambda: page_layout(appointments.appointments_page()),
    route="/appointments",
    title="Appointments | Appointment Manager",
)
app.add_page(
    lambda: page_layout(customers.customers_page()),
    route="/customers",
    title="Customers | Appointment Manager",
)
app.add_page(
    lambda: page_layout(providers.providers_page()),
    route="/providers",
    title="Providers | Appointment Manager",
)
app.add_page(
    lambda: page_layout(departments.departments_page()),
    route="/departments",
    title="Departments | Appointment Manager",
)
app.add_page(
    lambda: page_layout(business_settings.business_settings_page()),
    route="/settings/business",
    title="Business Settings | Appointment Manager",
)
app.add_page(
    lambda: page_layout(reports.reports_page()),
    route="/reports",
    title="Reports | Appointment Manager",
)
app.add_page(
    lambda: page_layout(archived_providers.archived_providers_page()),
    route="/providers/archived",
    title="Archived Providers | Appointment Manager",
)
app.add_page(
    lambda: page_layout(customer_profile.customer_profile_page()),
    route="/customers/[customer_id]",
    title="Customer Profile | Appointment Manager",
)