import reflex as rx
from app.states.dashboard_state import DashboardState
from app.models import Appointment
from app.pages.appointments import status_badge


def kpi_card(title: str, value: rx.Var[str], icon: str, color: str) -> rx.Component:
    """A card for displaying a key performance indicator."""
    return rx.el.div(
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.icon(icon, class_name=f"h-6 w-6 {color}"),
            class_name="flex items-center justify-between",
        ),
        rx.el.p(value, class_name="text-3xl font-bold text-gray-900 mt-2"),
        class_name="p-5 bg-white rounded-xl border border-gray-200 shadow-sm",
    )


def status_card(status: str, count: rx.Var[int], icon: str) -> rx.Component:
    """A card for displaying appointment status count."""
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-gray-500"),
            rx.el.p(status, class_name="text-sm font-medium text-gray-700"),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(count, class_name="text-2xl font-bold text-gray-900"),
        class_name="flex items-center justify-between p-4 bg-gray-50 rounded-lg",
    )


def recent_appointment_row(appointment: Appointment) -> rx.Component:
    """A row for the recent appointments list."""
    customer_name = DashboardState.customer_details.get(
        appointment["customer_id"], {}
    ).get("name", "N/A")
    provider_name = DashboardState.provider_details.get(
        appointment["provider_id"], "N/A"
    )
    return rx.el.div(
        rx.el.div(
            rx.el.p(customer_name, class_name="font-semibold text-gray-800 truncate"),
            rx.el.p(
                f"with {provider_name}", class_name="text-xs text-gray-500 truncate"
            ),
            class_name="flex-1 min-w-0",
        ),
        rx.el.div(
            rx.el.p(
                DashboardState.appointment_dates[appointment["id"]],
                class_name="text-sm text-gray-600",
            ),
            class_name="hidden md:block w-32 text-right",
        ),
        rx.el.div(status_badge(appointment["status"])),
        class_name="flex items-center justify-between gap-4 p-3 border-b border-gray-100",
    )


def provider_performance_row(provider_stats: dict) -> rx.Component:
    """A row for the provider performance list."""
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed={provider_stats['name']}",
                class_name="h-10 w-10 rounded-full",
            ),
            rx.el.p(provider_stats["name"], class_name="font-semibold text-gray-800"),
            class_name="flex items-center gap-3",
        ),
        rx.el.p(
            f"{provider_stats['appointment_count']} appointments",
            class_name="text-sm font-medium text-emerald-600",
        ),
        class_name="flex items-center justify-between p-3",
    )


def dashboard_page() -> rx.Component:
    """The main dashboard page UI."""
    return rx.el.div(
        rx.el.h1("Dashboard", class_name="text-2xl font-bold text-gray-900 mb-6"),
        rx.el.div(
            kpi_card(
                "Total Revenue",
                DashboardState.total_revenue,
                "dollar-sign",
                "text-emerald-600",
            ),
            kpi_card(
                "Total Appointments",
                DashboardState.total_appointments.to_string(),
                "calendar-check-2",
                "text-blue-600",
            ),
            kpi_card(
                "Active Providers",
                DashboardState.active_providers_count.to_string(),
                "user-cog",
                "text-amber-600",
            ),
            kpi_card(
                "Total Customers",
                DashboardState.total_customers.to_string(),
                "users",
                "text-cyan-600",
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Appointment Summary",
                        class_name="text-lg font-semibold text-gray-800 mb-4 px-1",
                    ),
                    rx.el.div(
                        status_card("Today", DashboardState.today_appointments, "sun"),
                        status_card(
                            "This Week",
                            DashboardState.this_week_appointments,
                            "calendar-days",
                        ),
                        status_card(
                            "This Month",
                            DashboardState.this_month_appointments,
                            "calendar-range",
                        ),
                        class_name="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6",
                    ),
                    rx.el.div(
                        status_card(
                            "Pending",
                            DashboardState.status_counts.get("Pending", 0),
                            "loader",
                        ),
                        status_card(
                            "Confirmed",
                            DashboardState.status_counts.get("Confirmed", 0),
                            "check_check",
                        ),
                        status_card(
                            "Completed",
                            DashboardState.status_counts.get("Completed", 0),
                            "square_check",
                        ),
                        status_card(
                            "Cancelled",
                            DashboardState.status_counts.get("Cancelled", 0),
                            "circle_x",
                        ),
                        status_card(
                            "No-Show",
                            DashboardState.status_counts.get("No-Show", 0),
                            "user-x",
                        ),
                        class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4",
                    ),
                    class_name="p-5 bg-white rounded-xl border border-gray-200 shadow-sm",
                ),
                class_name="lg:col-span-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Recent Activity",
                        class_name="text-lg font-semibold text-gray-800 mb-4 px-1",
                    ),
                    rx.el.div(
                        rx.foreach(
                            DashboardState.recent_appointments, recent_appointment_row
                        ),
                        class_name="bg-white rounded-xl border border-gray-200 shadow-sm mb-6",
                    ),
                    rx.el.h2(
                        "Top Providers",
                        class_name="text-lg font-semibold text-gray-800 mb-4 px-1",
                    ),
                    rx.el.div(
                        rx.foreach(
                            DashboardState.provider_performance,
                            provider_performance_row,
                        ),
                        class_name="bg-white rounded-xl border border-gray-200 shadow-sm divide-y divide-gray-100",
                    ),
                )
            ),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6",
        ),
        class_name="max-w-full w-full mx-auto",
        on_mount=DashboardState.on_load,
    )