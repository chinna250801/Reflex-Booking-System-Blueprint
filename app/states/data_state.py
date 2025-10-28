import reflex as rx
import uuid
from datetime import datetime, timedelta, time
from typing import Optional
from dateutil.relativedelta import relativedelta
from app.models import (
    Business,
    Department,
    Provider,
    Customer,
    Slot,
    Appointment,
    AvailabilityConfig,
    HistoryLog,
)
from datetime import datetime, time, timedelta

business_id = str(uuid.uuid4())
dept_med_id = str(uuid.uuid4())
dept_dental_id = str(uuid.uuid4())
provider1_id = str(uuid.uuid4())
provider2_id = str(uuid.uuid4())
provider3_id = str(uuid.uuid4())
cust1_id = str(uuid.uuid4())
cust2_id = str(uuid.uuid4())
cust3_id = str(uuid.uuid4())
mock_business = Business(
    id=business_id,
    legal_name="Wellness Group Inc.",
    display_name="Wellness Group",
    logo_url="/placeholder.svg",
    registration_number="U12345ABC67890",
    gstn="29ABCDE1234F1Z5",
    address="123 Health St, Med-City, 12345",
    contact_mobile="+1-202-555-0175",
    contact_email="contact@wellness.com",
    created_at=datetime.now(),
    updated_at=datetime.now(),
)
mock_departments = [
    Department(
        id=dept_med_id,
        business_id=business_id,
        name="General Medicine",
        description="Consultations and general health check-ups.",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    Department(
        id=dept_dental_id,
        business_id=business_id,
        name="Dental Care",
        description="Routine dental check-ups, cleaning, and treatments.",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]
mock_providers = [
    Provider(
        id=provider1_id,
        name="Dr. Alice Williams",
        department_ids=[dept_med_id],
        status="Active",
        bio="15 years of experience in general medicine.",
        contact_mobile="555-0101",
        contact_email="alice.w@wellness.com",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    Provider(
        id=provider2_id,
        name="Dr. Bob Brown",
        department_ids=[dept_dental_id],
        status="Active",
        bio="Specialist in cosmetic dentistry.",
        contact_mobile="555-0102",
        contact_email="bob.b@wellness.com",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    Provider(
        id=provider3_id,
        name="Dr. Charlie Davis",
        department_ids=[dept_med_id, dept_dental_id],
        status="Inactive",
        bio="General practitioner, currently on leave.",
        contact_mobile="555-0103",
        contact_email="charlie.d@wellness.com",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]
mock_customers = [
    Customer(
        id=cust1_id,
        full_name="John Smith",
        mobile="555-0111",
        email="john.smith@example.com",
        location="Downtown",
        age=34,
        gender="Male",
        address="123 Main St",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    Customer(
        id=cust2_id,
        full_name="Jane Doe",
        mobile="555-0112",
        email="jane.doe@example.com",
        location="Uptown",
        age=28,
        gender="Female",
        address="456 Oak Ave",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    Customer(
        id=cust3_id,
        full_name="Peter Jones",
        mobile="555-0113",
        email="peter.jones@example.com",
        location="Midtown",
        age=45,
        gender="Male",
        address="789 Pine Ln",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]
mock_availability_configs = {
    provider1_id: AvailabilityConfig(
        id=str(uuid.uuid4()),
        provider_id=provider1_id,
        month="2024-07",
        weekly_template={
            1: [(time(9, 0), time(12, 0)), (time(13, 0), time(17, 0))],
            2: [(time(9, 0), time(12, 0)), (time(13, 0), time(17, 0))],
            3: [(time(9, 0), time(12, 0))],
            4: [(time(9, 0), time(12, 0)), (time(13, 0), time(17, 0))],
            5: [(time(9, 0), time(13, 0))],
        },
        exceptions={},
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    provider2_id: AvailabilityConfig(
        id=str(uuid.uuid4()),
        provider_id=provider2_id,
        month="2024-07",
        weekly_template={
            0: [(time(10, 0), time(15, 0))],
            1: [(time(14, 0), time(18, 0))],
            3: [(time(10, 0), time(18, 0))],
            5: [(time(10, 0), time(14, 0))],
        },
        exceptions={},
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
}


def generate_slots_for_provider(
    provider_id: str, config: AvailabilityConfig, start_date: datetime, num_days: int
) -> list[Slot]:
    slots = []
    slot_duration = timedelta(minutes=30)
    for day in range(num_days):
        current_date = start_date + timedelta(days=day)
        day_of_week = current_date.weekday()
        time_ranges = config["weekly_template"].get(day_of_week, [])
        for start_time, end_time in time_ranges:
            current_slot_time = datetime.combine(current_date, start_time)
            end_slot_time = datetime.combine(current_date, end_time)
            while current_slot_time + slot_duration <= end_slot_time:
                slots.append(
                    Slot(
                        id=str(uuid.uuid4()),
                        provider_id=provider_id,
                        start_datetime=current_slot_time,
                        end_datetime=current_slot_time + slot_duration,
                        price_cents=5000 if provider_id == provider1_id else 7500,
                        is_booked=False,
                        calendar_month=current_date.strftime("%Y-%m"),
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                    )
                )
                current_slot_time += slot_duration
    return slots


today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
mock_slots = []
for provider_id, config in mock_availability_configs.items():
    mock_slots.extend(generate_slots_for_provider(provider_id, config, today, 60))
mock_appointments: list[Appointment] = []
mock_history_logs: list[HistoryLog] = []


def create_appointment(slot: Slot, customer_id: str, status: str):
    appointment_id = str(uuid.uuid4())
    appointment = Appointment(
        id=appointment_id,
        slot_id=slot["id"],
        provider_id=slot["provider_id"],
        customer_id=customer_id,
        status=status,
        created_at=datetime.now() - timedelta(days=5),
        updated_at=datetime.now() - timedelta(days=5),
        notes=f"This is a {status.lower()} appointment.",
    )
    slot["is_booked"] = True
    mock_appointments.append(appointment)
    mock_history_logs.append(
        HistoryLog(
            id=str(uuid.uuid4()),
            appointment_id=appointment_id,
            action="create",
            performed_by="System",
            user_type="System",
            timestamp=appointment["created_at"],
            new_status=status,
            details="Appointment created",
        )
    )


available_slots_p1 = [
    s
    for s in mock_slots
    if s["provider_id"] == provider1_id
    and (not s["is_booked"])
    and (s["start_datetime"] > today)
]
available_slots_p2 = [
    s
    for s in mock_slots
    if s["provider_id"] == provider2_id
    and (not s["is_booked"])
    and (s["start_datetime"] > today)
]
if len(available_slots_p1) > 2:
    create_appointment(available_slots_p1[0], cust1_id, "Pending")
    create_appointment(available_slots_p1[1], cust2_id, "Confirmed")
    create_appointment(available_slots_p1[2], cust3_id, "Completed")
if len(available_slots_p2) > 0:
    create_appointment(available_slots_p2[0], cust1_id, "No-Show")


class DataState(rx.State):
    """Holds all the data for the application."""

    businesses: list[Business] = [mock_business]
    departments: list[Department] = mock_departments
    providers: list[Provider] = mock_providers
    customers: list[Customer] = mock_customers
    slots: list[Slot] = mock_slots
    appointments: list[Appointment] = mock_appointments
    availability_configs: dict[str, AvailabilityConfig] = mock_availability_configs
    history_logs: list[HistoryLog] = mock_history_logs
    selected_provider_id: str = ""
    selected_department_id: str = ""
    selected_month: str = datetime.now().strftime("%Y-%m")
    calendar_view: str = "month"
    date_range_filter: tuple = (None, None)
    status_filter: str = "all"

    def _get_department_by_id(self, department_id: str) -> Optional[Department]:
        return next((d for d in self.departments if d["id"] == department_id), None)

    def _get_provider_by_id(self, provider_id: str) -> Optional[Provider]:
        return next((p for p in self.providers if p["id"] == provider_id), None)

    def _get_slot_by_id(self, slot_id: str) -> Optional[Slot]:
        return next((s for s in self.slots if s["id"] == slot_id), None)

    def _get_appointment_by_id(self, appointment_id: str) -> Optional[Appointment]:
        return next((a for a in self.appointments if a["id"] == appointment_id), None)

    def _log_history(
        self,
        appointment_id: str,
        action: str,
        performed_by: str,
        user_type: str,
        old_status: Optional[str] = None,
        new_status: Optional[str] = None,
        details: Optional[str] = None,
    ):
        self.history_logs.append(
            HistoryLog(
                id=str(uuid.uuid4()),
                appointment_id=appointment_id,
                action=action,
                performed_by=performed_by,
                user_type=user_type,
                timestamp=datetime.now(),
                old_status=old_status,
                new_status=new_status,
                details=details,
            )
        )

    @rx.event
    def book_slot(
        self,
        customer_id: str,
        slot_id: str,
        performed_by: str = "System",
        user_type: str = "Customer",
    ) -> Optional[str]:
        slot = self._get_slot_by_id(slot_id)
        if not slot:
            return "Error: Slot not found."
        if slot["is_booked"]:
            return "Error: Slot is already booked."
        provider = self._get_provider_by_id(slot["provider_id"])
        if not provider or provider["status"] != "Active":
            return "Error: Provider is not active."
        customer_appointments = [
            a
            for a in self.appointments
            if a["customer_id"] == customer_id
            and a["provider_id"] == provider["id"]
            and (a["status"] not in ["Cancelled", "Completed", "No-Show"])
        ]
        for appt in customer_appointments:
            appt_slot = self._get_slot_by_id(appt["slot_id"])
            if appt_slot and (
                not (
                    slot["end_datetime"] <= appt_slot["start_datetime"]
                    or slot["start_datetime"] >= appt_slot["end_datetime"]
                )
            ):
                return (
                    "Error: Customer has an overlapping appointment with this provider."
                )
        slot["is_booked"] = True
        appointment_id = str(uuid.uuid4())
        new_appointment = Appointment(
            id=appointment_id,
            slot_id=slot_id,
            provider_id=slot["provider_id"],
            customer_id=customer_id,
            status="Pending",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            notes="Appointment booked.",
        )
        self.appointments.append(new_appointment)
        self._log_history(
            appointment_id,
            "create",
            performed_by,
            user_type,
            new_status="Pending",
            details="Appointment created.",
        )
        return None

    @rx.event
    def change_appointment_status(
        self, appointment_id: str, new_status: str, performed_by: str, user_type: str
    ) -> Optional[str]:
        appointment = self._get_appointment_by_id(appointment_id)
        if not appointment:
            return "Error: Appointment not found."
        old_status = appointment["status"]
        valid_transitions = {
            "Pending": ["Confirmed", "Cancelled", "Completed", "No-Show"],
            "Confirmed": ["Cancelled", "Completed", "No-Show"],
            "No-Show": ["Completed"],
        }
        if old_status in ["Cancelled", "Completed"]:
            return (
                f"Error: Cannot change status from a terminal state ('{old_status}')."
            )
        if new_status not in valid_transitions.get(old_status, []):
            return f"Error: Invalid status transition from '{old_status}' to '{new_status}'."
        appointment["status"] = new_status
        appointment["updated_at"] = datetime.now()
        if new_status == "Cancelled":
            slot = self._get_slot_by_id(appointment["slot_id"])
            if slot:
                slot["is_booked"] = False
        self._log_history(
            appointment["id"],
            "status_change",
            performed_by,
            user_type,
            old_status,
            new_status,
        )
        return None

    @rx.event
    def edit_appointment_time(
        self, appointment_id: str, new_slot_id: str, performed_by: str, user_type: str
    ) -> Optional[str]:
        appointment = self._get_appointment_by_id(appointment_id)
        if not appointment:
            return "Error: Appointment not found."
        if appointment["status"] in ["Cancelled", "Completed"]:
            return f"Error: Cannot edit a '{appointment['status']}' appointment."
        new_slot = self._get_slot_by_id(new_slot_id)
        if not new_slot:
            return "Error: New slot not found."
        if new_slot["is_booked"]:
            return "Error: New slot is already booked."
        if new_slot["provider_id"] != appointment["provider_id"]:
            return "Error: Cannot change provider when editing time."
        old_slot = self._get_slot_by_id(appointment["slot_id"])
        if old_slot:
            old_slot["is_booked"] = False
        new_slot["is_booked"] = True
        appointment["slot_id"] = new_slot_id
        appointment["updated_at"] = datetime.now()
        details = f"Time changed from {(old_slot['start_datetime'] if old_slot else 'N/A')} to {new_slot['start_datetime']}"
        self._log_history(
            appointment["id"], "update", performed_by, user_type, details=details
        )
        return None

    @rx.event
    def archive_provider(self, provider_id: str) -> Optional[str]:
        provider = self._get_provider_by_id(provider_id)
        if not provider:
            return "Error: Provider not found."
        has_active_appointments = any(
            (
                a["provider_id"] == provider_id
                and a["status"] in ["Pending", "Confirmed"]
                for a in self.appointments
            )
        )
        if has_active_appointments:
            return (
                "Error: Cannot archive provider with pending or confirmed appointments."
            )
        provider["status"] = "Archived"
        provider["updated_at"] = datetime.now()
        return None