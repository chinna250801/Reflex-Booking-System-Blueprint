import reflex as rx
from typing import TypedDict
from app.states.data_state import DataState


class NavItem(TypedDict):
    name: str
    icon: str
    route: str


class AppState(DataState):
    """The base state for the application."""

    sidebar_open: bool = False
    nav_items: list[NavItem] = [
        {"name": "Dashboard", "icon": "layout-dashboard", "route": "/"},
        {"name": "Calendar", "icon": "calendar-days", "route": "/calendar"},
        {"name": "Appointments", "icon": "calendar-check-2", "route": "/appointments"},
        {"name": "Customers", "icon": "users", "route": "/customers"},
        {"name": "Providers", "icon": "user-cog", "route": "/providers"},
        {"name": "Departments", "icon": "building", "route": "/departments"},
        {
            "name": "Business Settings",
            "icon": "settings",
            "route": "/settings/business",
        },
        {"name": "Reports", "icon": "bar-chart-3", "route": "/reports"},
        {
            "name": "Archived Providers",
            "icon": "archive",
            "route": "/providers/archived",
        },
    ]

    @rx.var
    def current_page_title(self) -> str:
        """Returns the title of the current page."""
        current_path = self.router.page.path
        for item in self.nav_items:
            if item["route"] == current_path:
                return item["name"]
        if "settings" in current_path:
            return "Business Settings"
        if "archived" in current_path:
            return "Archived Providers"
        return "Dashboard"

    @rx.event
    def toggle_sidebar(self):
        """Toggles the visibility of the sidebar on mobile."""
        self.sidebar_open = not self.sidebar_open