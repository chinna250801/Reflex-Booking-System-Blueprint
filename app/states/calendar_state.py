import reflex as rx
from datetime import datetime
from app.states.data_state import DataState
from app.models import Slot, Customer
import calendar
from typing import Optional, TypedDict
from dateutil.relativedelta import relativedelta


class FormattedSlot(TypedDict):
    id: str
    time_str: str
    is_booked: bool
    raw_slot: Slot


class DaySlots(TypedDict):
    visible: list[FormattedSlot]
    overflow: int


class CalendarState(DataState):
    """State for managing the calendar and booking UI."""

    show_booking_modal: bool = False
    show_availability_modal: bool = False
    booking_slot: Optional[Slot] = None
    booking_customer_id: str = ""
    booking_error: str = ""
    availability_provider_id: str = ""
    availability_month: str = ""
    weekly_template: dict[int, list[tuple[str, str]]] = {}
    calendar_weeks: list[list[Optional[int]]] = []
    slots_by_day: dict[int, DaySlots] = {}

    @rx.var
    def selected_provider_name(self) -> str:
        if not self.selected_provider_id:
            return "Provider not selected"
        provider = self._get_provider_by_id(self.selected_provider_id)
        return provider["name"] if provider else "Unknown Provider"

    def _build_calendar_data(self):
        """Pre-computes calendar grid and formatted slots data."""
        year, month = map(int, self.selected_month.split("-"))
        cal = calendar.Calendar()
        self.calendar_weeks = cal.monthdayscalendar(year, month)
        slots_map: dict[int, DaySlots] = {}
        if not self.selected_provider_id:
            self.slots_by_day = {}
            return
        day_slots: dict[int, list[Slot]] = {}
        for slot in self.slots:
            is_correct_provider = slot["provider_id"] == self.selected_provider_id
            slot_dt = slot["start_datetime"]
            if (
                is_correct_provider
                and slot_dt.year == year
                and (slot_dt.month == month)
            ):
                day = slot_dt.day
                if day not in day_slots:
                    day_slots[day] = []
                day_slots[day].append(slot)
        for day, slots in day_slots.items():
            slots.sort(key=lambda s: s["start_datetime"])
            formatted_slots = [
                FormattedSlot(
                    id=s["id"],
                    time_str=s["start_datetime"].strftime("%H:%M"),
                    is_booked=s["is_booked"],
                    raw_slot=s,
                )
                for s in slots
            ]
            slots_map[day] = {
                "visible": formatted_slots[:4],
                "overflow": max(0, len(formatted_slots) - 4),
            }
        self.slots_by_day = slots_map

    @rx.event
    def on_calendar_load(self):
        """Loads data and builds the calendar on page load."""
        if not self.selected_provider_id and self.providers:
            self.selected_provider_id = self.providers[0]["id"]
        self._build_calendar_data()

    @rx.event
    def handle_provider_change(self, provider_id: str):
        """Handles provider selection change."""
        self.selected_provider_id = provider_id
        self._build_calendar_data()

    @rx.event
    def change_month(self, amount: int):
        """Handles month navigation."""
        current_date = datetime.strptime(self.selected_month, "%Y-%m")
        new_date = current_date + relativedelta(months=amount)
        self.selected_month = new_date.strftime("%Y-%m")
        self._build_calendar_data()

    @rx.event
    def open_booking_modal(self, slot_data: FormattedSlot):
        self.booking_slot = slot_data["raw_slot"]
        if self.customers:
            self.booking_customer_id = self.customers[0]["id"]
        self.booking_error = ""
        self.show_booking_modal = True

    @rx.event
    def close_booking_modal(self):
        self.show_booking_modal = False
        self.booking_slot = None
        self.booking_error = ""

    @rx.event
    def confirm_booking(self):
        if not self.booking_slot or not self.booking_customer_id:
            self.booking_error = "Slot or customer not selected."
            return
        result = self.book_slot(
            self.booking_customer_id, self.booking_slot["id"], "WebApp", "Admin"
        )
        if result:
            self.booking_error = result
            yield rx.toast(result, duration=5000)
        else:
            yield rx.toast("Appointment booked successfully!")
            yield CalendarState.close_booking_modal()
        self._build_calendar_data()

    @rx.event
    def open_availability_modal(self):
        if not self.selected_provider_id:
            yield rx.toast("Please select a provider first.", duration=3000)
            return
        self.availability_provider_id = self.selected_provider_id
        self.availability_month = self.selected_month
        config = self.availability_configs.get(self.availability_provider_id)
        if config and config.get("weekly_template"):
            current_template_raw = config["weekly_template"]
            self.weekly_template = {
                day: [
                    (start.strftime("%H:%M"), end.strftime("%H:%M"))
                    for start, end in ranges
                ]
                for day, ranges in current_template_raw.items()
            }
        else:
            self.weekly_template = {}
        self.show_availability_modal = True

    @rx.event
    def close_availability_modal(self):
        self.show_availability_modal = False
        self.weekly_template = {}