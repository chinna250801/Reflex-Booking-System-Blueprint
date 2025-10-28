import reflex as rx
from app.states.data_state import DataState
from app.models import Appointment
from datetime import datetime, timedelta


class DashboardState(DataState):
    """State for the dashboard page, providing analytical data."""

    @rx.event
    def on_load(self):
        """Placeholder for on-load event for the dashboard."""
        pass

    @rx.var
    def total_revenue(self) -> str:
        """Calculates the total revenue from completed appointments."""
        total = 0
        for appt in self.appointments:
            if appt["status"] == "Completed":
                slot = self._get_slot_by_id(appt["slot_id"])
                if slot:
                    total += slot["price_cents"]
        return f"${total / 100:.2f}"

    @rx.var
    def total_appointments(self) -> int:
        """Returns the total number of appointments."""
        return len(self.appointments)

    @rx.var
    def active_providers_count(self) -> int:
        """Returns the count of active providers."""
        return len([p for p in self.providers if p["status"] == "Active"])

    @rx.var
    def total_customers(self) -> int:
        """Returns the total number of customers."""
        return len(self.customers)

    @rx.var
    def status_counts(self) -> dict[str, int]:
        """Counts appointments by status."""
        counts = {
            "Pending": 0,
            "Confirmed": 0,
            "Completed": 0,
            "Cancelled": 0,
            "No-Show": 0,
        }
        for appt in self.appointments:
            if appt["status"] in counts:
                counts[appt["status"]] += 1
        return counts

    @rx.var
    def today_appointments(self) -> int:
        """Counts appointments scheduled for today."""
        today = datetime.now().date()
        count = 0
        for appt in self.appointments:
            slot = self._get_slot_by_id(appt["slot_id"])
            if slot and slot["start_datetime"].date() == today:
                count += 1
        return count

    @rx.var
    def this_week_appointments(self) -> int:
        """Counts appointments for the current week (Mon-Sun)."""
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        count = 0
        for appt in self.appointments:
            slot = self._get_slot_by_id(appt["slot_id"])
            if slot and start_of_week <= slot["start_datetime"].date() <= end_of_week:
                count += 1
        return count

    @rx.var
    def this_month_appointments(self) -> int:
        """Counts appointments for the current month."""
        current_month = datetime.now().month
        current_year = datetime.now().year
        count = 0
        for appt in self.appointments:
            slot = self._get_slot_by_id(appt["slot_id"])
            if (
                slot
                and slot["start_datetime"].month == current_month
                and (slot["start_datetime"].year == current_year)
            ):
                count += 1
        return count

    @rx.var
    def recent_appointments(self) -> list[Appointment]:
        """Returns the 5 most recent appointments."""
        sorted_appts = sorted(
            self.appointments, key=lambda a: a["created_at"], reverse=True
        )
        return sorted_appts[:5]

    @rx.var
    def provider_performance(self) -> list[dict]:
        """Ranks providers by the number of completed appointments."""
        performance = {}
        for provider in self.providers:
            if provider["status"] == "Active":
                performance[provider["id"]] = {
                    "name": provider["name"],
                    "appointment_count": 0,
                }
        for appt in self.appointments:
            if appt["provider_id"] in performance:
                performance[appt["provider_id"]]["appointment_count"] += 1
        sorted_performance = sorted(
            performance.values(), key=lambda x: x["appointment_count"], reverse=True
        )
        return sorted_performance[:3]

    @rx.var
    def customer_details(self) -> dict[str, dict]:
        """A map of customer IDs to their name and avatar URL."""
        return {
            c["id"]: {
                "name": c["full_name"],
                "avatar": f"https://api.dicebear.com/9.x/initials/svg?seed={c['full_name']}",
            }
            for c in self.customers
        }

    @rx.var
    def provider_details(self) -> dict[str, str]:
        """A map of provider IDs to their name."""
        return {p["id"]: p["name"] for p in self.providers}

    @rx.var
    def appointment_dates(self) -> dict[str, str]:
        """A map of appointment IDs to formatted date strings."""
        dates = {}
        for appt in self.appointments:
            slot = self._get_slot_by_id(appt["slot_id"])
            if slot:
                dates[appt["id"]] = slot["start_datetime"].strftime("%B %d, %Y")
        return dates