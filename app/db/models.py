from __future__ import annotations
import datetime
import uuid
from typing import TYPE_CHECKING, Any, Optional
from sqlmodel import Field, Relationship, SQLModel, JSON, Column
from sqlalchemy import func
from sqlalchemy.schema import UniqueConstraint

if TYPE_CHECKING:
    from app.db.models import (
        BusinessDB,
        DepartmentDB,
        ProviderDB,
        CustomerDB,
        SlotDB,
        AppointmentDB,
    )
WeeklyTemplate = dict[int, list[tuple[str, str]]]
Exceptions = dict[str, list[tuple[str, str]]]


class BusinessDB(SQLModel, table=True):
    __tablename__ = "businesses"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    legal_name: str
    display_name: str
    logo_url: Optional[str] = Field(default=None)
    registration_number: Optional[str] = Field(default=None)
    gstn: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    contact_mobile: Optional[str] = Field(default=None)
    contact_email: Optional[str] = Field(default=None)
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow, nullable=False
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": func.now()},
    )
    departments: list[DepartmentDB] = Relationship(back_populates="business")


class ProviderDepartmentLinkDB(SQLModel, table=True):
    __tablename__ = "provider_department_link"
    provider_id: uuid.UUID = Field(foreign_key="providers.id", primary_key=True)
    department_id: uuid.UUID = Field(foreign_key="departments.id", primary_key=True)


class DepartmentDB(SQLModel, table=True):
    __tablename__ = "departments"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    description: Optional[str] = Field(default=None)
    business_id: uuid.UUID = Field(foreign_key="businesses.id")
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow, nullable=False
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": func.now()},
    )
    business: BusinessDB = Relationship(back_populates="departments")
    providers: list[ProviderDB] = Relationship(
        back_populates="departments", link_model=ProviderDepartmentLinkDB
    )


class ProviderDB(SQLModel, table=True):
    __tablename__ = "providers"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    status: str = Field(default="Active", index=True)
    bio: Optional[str] = Field(default=None)
    contact_mobile: Optional[str] = Field(default=None)
    contact_email: Optional[str] = Field(default=None)
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow, nullable=False
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": func.now()},
    )
    departments: list[DepartmentDB] = Relationship(
        back_populates="providers", link_model=ProviderDepartmentLinkDB
    )
    slots: list[SlotDB] = Relationship(back_populates="provider")
    appointments: list[AppointmentDB] = Relationship(back_populates="provider")


class CustomerDB(SQLModel, table=True):
    __tablename__ = "customers"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    full_name: str
    mobile: str = Field(index=True, nullable=False)
    email: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
    gender: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow, nullable=False
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": func.now()},
    )
    appointments: list[AppointmentDB] = Relationship(back_populates="customer")


class SlotDB(SQLModel, table=True):
    __tablename__ = "slots"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    provider_id: uuid.UUID = Field(foreign_key="providers.id", index=True)
    start_datetime: datetime.datetime = Field(index=True)
    end_datetime: datetime.datetime
    price_cents: int
    is_booked: bool = Field(default=False)
    calendar_month: str = Field(index=True)
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow, nullable=False
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": func.now()},
    )
    provider: ProviderDB = Relationship(back_populates="slots")
    appointment: Optional[AppointmentDB] = Relationship(back_populates="slot")


class AppointmentDB(SQLModel, table=True):
    __tablename__ = "appointments"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    slot_id: uuid.UUID = Field(foreign_key="slots.id", unique=True)
    provider_id: uuid.UUID = Field(foreign_key="providers.id", index=True)
    customer_id: uuid.UUID = Field(foreign_key="customers.id", index=True)
    status: str = Field(default="Pending", index=True)
    notes: Optional[str] = Field(default=None)
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow, nullable=False, index=True
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": func.now()},
    )
    slot: SlotDB = Relationship(back_populates="appointment")
    provider: ProviderDB = Relationship(back_populates="appointments")
    customer: CustomerDB = Relationship(back_populates="appointments")
    history_logs: list[HistoryLogDB] = Relationship(back_populates="appointment")


class AvailabilityConfigDB(SQLModel, table=True):
    __tablename__ = "availability_configs"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    provider_id: uuid.UUID = Field(foreign_key="providers.id", index=True)
    month: str = Field(index=True)
    weekly_template: WeeklyTemplate | None = Field(default=None, sa_column=Column(JSON))
    exceptions: Exceptions | None = Field(default=None, sa_column=Column(JSON))
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow, nullable=False
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": func.now()},
    )
    __table_args__ = (UniqueConstraint("provider_id", "month"),)


class HistoryLogDB(SQLModel, table=True):
    __tablename__ = "history_logs"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    appointment_id: uuid.UUID = Field(foreign_key="appointments.id", index=True)
    action: str
    performed_by: str
    user_type: str
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow, nullable=False, index=True
    )
    old_status: Optional[str] = Field(default=None)
    new_status: Optional[str] = Field(default=None)
    details: Optional[str] = Field(default=None)
    appointment: AppointmentDB = Relationship(back_populates="history_logs")