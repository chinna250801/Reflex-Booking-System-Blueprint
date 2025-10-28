import reflex as rx
from dataclasses import dataclass, field
from datetime import datetime, time
from typing import Optional


@dataclass
class Business:
    id: str
    legal_name: str
    display_name: str
    logo_url: str
    registration_number: str
    gstn: str
    address: str
    contact_mobile: str
    contact_email: str


@dataclass
class Department:
    id: str
    business_id: str
    name: str
    description: str


@dataclass
class Provider:
    id: str
    name: str
    department_ids: list[str]
    status: str
    bio: str
    contact_mobile: str
    contact_email: str


@dataclass
class Customer:
    id: str
    full_name: str
    mobile: str
    email: Optional[str] = None
    location: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    address: Optional[str] = None


@dataclass
class Slot:
    id: str
    provider_id: str
    start_datetime: datetime
    end_datetime: datetime
    price_cents: int
    is_booked: bool
    calendar_month: str


@dataclass
class Appointment:
    id: str
    slot_id: str
    provider_id: str
    customer_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None


@dataclass
class AvailabilityConfig:
    provider_id: str
    month: str
    weekly_template: dict[int, list[tuple[time, time]]]
    exceptions: dict[str, list[tuple[time, time]]] = field(default_factory=dict)


@dataclass
class HistoryLog:
    id: str
    appointment_id: str
    action: str
    performed_by: str
    user_type: str
    timestamp: datetime
    old_status: Optional[str] = None
    new_status: Optional[str] = None
    details: Optional[str] = None