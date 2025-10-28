from __future__ import annotations
from typing import TypedDict, Optional
import uuid
import datetime


class Business(TypedDict):
    id: str
    legal_name: str
    display_name: str
    logo_url: Optional[str]
    registration_number: Optional[str]
    gstn: Optional[str]
    address: Optional[str]
    contact_mobile: Optional[str]
    contact_email: Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class Department(TypedDict):
    id: str
    business_id: str
    name: str
    description: Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ProviderDepartmentLink(TypedDict):
    provider_id: str
    department_id: str


class Provider(TypedDict):
    id: str
    name: str
    department_ids: list[str]
    status: str
    bio: Optional[str]
    contact_mobile: Optional[str]
    contact_email: Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class Customer(TypedDict):
    id: str
    full_name: str
    mobile: str
    email: Optional[str]
    location: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    address: Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class Slot(TypedDict):
    id: str
    provider_id: str
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
    price_cents: int
    is_booked: bool
    calendar_month: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class Appointment(TypedDict):
    id: str
    slot_id: str
    provider_id: str
    customer_id: str
    status: str
    notes: Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class AvailabilityConfig(TypedDict):
    id: str
    provider_id: str
    month: str
    weekly_template: dict[int, list[tuple[datetime.time, datetime.time]]]
    exceptions: dict
    created_at: datetime.datetime
    updated_at: datetime.datetime


class HistoryLog(TypedDict):
    id: str
    appointment_id: str
    action: str
    performed_by: str
    user_type: str
    timestamp: datetime.datetime
    old_status: Optional[str]
    new_status: Optional[str]
    details: Optional[str]