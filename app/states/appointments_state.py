import reflex as rx
from app.states.data_state import DataState
from app.models import Appointment, Customer
from typing import Optional


class AppointmentsState(DataState):
    """State for managing the appointments page."""

    search_term: str = ""
    status_filter: str = "all"
    status_options: list[str] = [
        "Pending",
        "Confirmed",
        "Completed",
        "Cancelled",
        "No-Show",
    ]

    @rx.event
    def on_load(self):
        """Event handler for page load."""
        pass

    @rx.var
    def filtered_appointments(self) -> list[Appointment]:
        """Returns appointments filtered by search term and status."""
        appointments = self.appointments
        if self.status_filter != "all":
            appointments = [
                a for a in appointments if a["status"] == self.status_filter
            ]
        if self.search_term.strip():
            term = self.search_term.lower()
            customer_ids_to_match = {
                c["id"] for c in self.customers if term in c["full_name"].lower()
            }
            appointments = [
                a for a in appointments if a["customer_id"] in customer_ids_to_match
            ]
        return sorted(appointments, key=lambda a: a["created_at"], reverse=True)

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
    def appointment_datetimes(self) -> dict[str, dict]:
        """A map of appointment IDs to formatted date and time strings."""
        details = {}
        for appt in self.appointments:
            slot = self._get_slot_by_id(appt["slot_id"])
            if slot:
                details[appt["id"]] = {
                    "date": slot["start_datetime"].strftime("%B %d, %Y"),
                    "time": f"{slot['start_datetime'].strftime('%I:%M %p')} - {slot['end_datetime'].strftime('%I:%M %p')}",
                }
        return details

    @rx.var
    def appointment_prices(self) -> dict[str, str]:
        """A map of appointment IDs to formatted price strings."""
        prices = {}
        for appt in self.appointments:
            slot = self._get_slot_by_id(appt["slot_id"])
            if slot:
                prices[appt["id"]] = f"${slot['price_cents'] / 100:.2f}"
        return prices

    @rx.event
    def update_status(self, appointment_id: str, new_status: str):
        result = self.change_appointment_status(
            appointment_id, new_status, performed_by="Admin", user_type="WebApp"
        )
        if result:
            return rx.toast(result, duration=4000)
        return rx.toast(f"Appointment status updated to {new_status}.")