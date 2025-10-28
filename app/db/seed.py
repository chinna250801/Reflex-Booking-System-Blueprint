import uuid
from datetime import datetime, time, timedelta
from sqlmodel import select
from app.db.database import get_session
from app.db.models import (
    BusinessDB,
    DepartmentDB,
    ProviderDB,
    CustomerDB,
    SlotDB,
    AppointmentDB,
    AvailabilityConfigDB,
    HistoryLogDB,
)


def generate_slots_for_provider(
    provider_id: uuid.UUID, config: dict, start_date: datetime, num_days: int
) -> list[SlotDB]:
    slots = []
    slot_duration = timedelta(minutes=30)
    for day in range(num_days):
        current_date = start_date + timedelta(days=day)
        day_of_week = current_date.weekday()
        time_ranges_str = config.get(day_of_week, [])
        time_ranges = []
        for start_str, end_str in time_ranges_str:
            start_time = datetime.strptime(start_str, "%H:%M:%S").time()
            end_time = datetime.strptime(end_str, "%H:%M:%S").time()
            time_ranges.append((start_time, end_time))
        for start_time, end_time in time_ranges:
            current_slot_time = datetime.combine(current_date, start_time)
            end_slot_time = datetime.combine(current_date, end_time)
            while current_slot_time + slot_duration <= end_slot_time:
                slots.append(
                    SlotDB(
                        provider_id=provider_id,
                        start_datetime=current_slot_time,
                        end_datetime=current_slot_time + slot_duration,
                        price_cents=5000 if str(provider_id).startswith("a") else 7500,
                        is_booked=False,
                        calendar_month=current_date.strftime("%Y-%m"),
                    )
                )
                current_slot_time += slot_duration
    return slots


def seed_database():
    with get_session() as session:
        if session.exec(select(BusinessDB)).first():
            print("Database already seeded.")
            return
        print("Seeding database...")
        business = BusinessDB(
            legal_name="Wellness Group Inc.",
            display_name="Wellness Group",
            logo_url="/placeholder.svg",
            registration_number="U12345ABC67890",
            gstn="29ABCDE1234F1Z5",
            address="123 Health St, Med-City, 12345",
            contact_mobile="+1-202-555-0175",
            contact_email="contact@wellness.com",
        )
        session.add(business)
        session.commit()
        session.refresh(business)
        dept_med = DepartmentDB(
            name="General Medicine",
            description="Consultations and general health check-ups.",
            business_id=business.id,
        )
        dept_dental = DepartmentDB(
            name="Dental Care",
            description="Routine dental check-ups, cleaning, and treatments.",
            business_id=business.id,
        )
        session.add_all([dept_med, dept_dental])
        session.commit()
        session.refresh(dept_med)
        session.refresh(dept_dental)
        provider1 = ProviderDB(
            name="Dr. Alice Williams",
            status="Active",
            bio="15 years of experience in general medicine.",
            contact_mobile="555-0101",
            contact_email="alice.w@wellness.com",
            departments=[dept_med],
        )
        provider2 = ProviderDB(
            name="Dr. Bob Brown",
            status="Active",
            bio="Specialist in cosmetic dentistry.",
            contact_mobile="555-0102",
            contact_email="bob.b@wellness.com",
            departments=[dept_dental],
        )
        provider3 = ProviderDB(
            name="Dr. Charlie Davis",
            status="Inactive",
            bio="General practitioner, currently on leave.",
            contact_mobile="555-0103",
            contact_email="charlie.d@wellness.com",
            departments=[dept_med, dept_dental],
        )
        session.add_all([provider1, provider2, provider3])
        session.commit()
        session.refresh(provider1)
        session.refresh(provider2)
        session.refresh(provider3)
        cust1 = CustomerDB(
            full_name="John Smith", mobile="555-0111", email="john.smith@example.com"
        )
        cust2 = CustomerDB(
            full_name="Jane Doe", mobile="555-0112", email="jane.doe@example.com"
        )
        cust3 = CustomerDB(
            full_name="Peter Jones", mobile="555-0113", email="peter.jones@example.com"
        )
        session.add_all([cust1, cust2, cust3])
        session.commit()
        session.refresh(cust1)
        session.refresh(cust2)
        session.refresh(cust3)
        avail_p1 = AvailabilityConfigDB(
            provider_id=provider1.id,
            month="2024-07",
            weekly_template={
                "1": [("09:00:00", "12:00:00"), ("13:00:00", "17:00:00")],
                "2": [("09:00:00", "12:00:00"), ("13:00:00", "17:00:00")],
                "3": [("09:00:00", "12:00:00")],
                "4": [("09:00:00", "12:00:00"), ("13:00:00", "17:00:00")],
                "5": [("09:00:00", "13:00:00")],
            },
            exceptions={},
        )
        avail_p2 = AvailabilityConfigDB(
            provider_id=provider2.id,
            month="2024-07",
            weekly_template={
                "0": [("10:00:00", "15:00:00")],
                "1": [("14:00:00", "18:00:00")],
                "3": [("10:00:00", "18:00:00")],
                "5": [("10:00:00", "14:00:00")],
            },
            exceptions={},
        )
        session.add_all([avail_p1, avail_p2])
        session.commit()
        session.refresh(avail_p1)
        session.refresh(avail_p2)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        all_slots = []
        all_slots.extend(
            generate_slots_for_provider(
                provider1.id, avail_p1.weekly_template, today, 60
            )
        )
        all_slots.extend(
            generate_slots_for_provider(
                provider2.id, avail_p2.weekly_template, today, 60
            )
        )
        session.add_all(all_slots)
        session.commit()
        available_slots_p1 = [
            s
            for s in all_slots
            if s.provider_id == provider1.id
            and (not s.is_booked)
            and (s.start_datetime > today)
        ]
        available_slots_p2 = [
            s
            for s in all_slots
            if s.provider_id == provider2.id
            and (not s.is_booked)
            and (s.start_datetime > today)
        ]
        appointments_to_add = []
        history_logs_to_add = []

        def create_appt(slot: SlotDB, customer: CustomerDB, status: str):
            slot.is_booked = True
            appt = AppointmentDB(
                slot_id=slot.id,
                provider_id=slot.provider_id,
                customer_id=customer.id,
                status=status,
                notes=f"This is a {status.lower()} appointment.",
            )
            appointments_to_add.append(appt)
            session.add(appt)
            session.commit()
            session.refresh(appt)
            history_log = HistoryLogDB(
                appointment_id=appt.id,
                action="create",
                performed_by="System",
                user_type="System",
                new_status=status,
                details="Appointment created during seeding",
            )
            history_logs_to_add.append(history_log)

        if len(available_slots_p1) > 2:
            create_appt(available_slots_p1[0], cust1, "Pending")
            create_appt(available_slots_p1[1], cust2, "Confirmed")
            create_appt(available_slots_p1[2], cust3, "Completed")
        if len(available_slots_p2) > 0:
            create_appt(available_slots_p2[0], cust1, "No-Show")
        session.add_all(history_logs_to_add)
        session.commit()
        print("Database seeding complete!")