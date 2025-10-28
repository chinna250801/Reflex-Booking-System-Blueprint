import reflex as rx
import uuid
from typing import Optional
from app.states.data_state import DataState
from app.models import Department, Provider


class ManagementState(DataState):
    """State for managing departments and providers."""

    show_department_modal: bool = False
    department_form_id: str = ""
    department_name: str = ""
    department_description: str = ""
    department_error: str = ""
    show_provider_modal: bool = False
    provider_form_id: str = ""
    provider_name: str = ""
    provider_bio: str = ""
    provider_contact_mobile: str = ""
    provider_contact_email: str = ""
    provider_department_ids: list[str] = []
    provider_status: str = "Active"
    provider_error: str = ""
    show_delete_confirmation: bool = False
    item_to_delete_id: str = ""
    delete_item_type: str = ""
    delete_warning_message: str = ""

    @rx.var
    def department_form_is_edit(self) -> bool:
        return self.department_form_id != ""

    @rx.var
    def provider_form_is_edit(self) -> bool:
        return self.provider_form_id != ""

    @rx.var
    def active_providers(self) -> list[Provider]:
        return [p for p in self.providers if p.status != "Archived"]

    def _get_department_names_for_provider(self, dept_ids: list[str]) -> str:
        """A helper method to get a comma-separated string of department names for a provider."""
        names = [d.name for d in self.departments if d.id in dept_ids]
        return ", ".join(names)

    @rx.var
    def provider_department_names(self) -> dict[str, str]:
        """A computed var mapping provider IDs to their department names string."""
        provider_dept_names = {}
        for p in self.providers:
            provider_dept_names[p.id] = self._get_department_names_for_provider(
                p.department_ids
            )
        return provider_dept_names

    def _get_department_names_for_provider(self, dept_ids: list[str]) -> str:
        """A helper method to get a comma-separated string of department names for a provider."""
        names = [d.name for d in self.departments if d.id in dept_ids]
        return ", ".join(names)

    @rx.var
    def provider_department_names(self) -> dict[str, str]:
        """A computed var mapping provider IDs to their department names string."""
        provider_dept_names = {}
        for p in self.providers:
            provider_dept_names[p.id] = self._get_department_names_for_provider(
                p.department_ids
            )
        return provider_dept_names

    def _clear_department_form(self):
        self.department_form_id = ""
        self.department_name = ""
        self.department_description = ""
        self.department_error = ""

    def _clear_provider_form(self):
        self.provider_form_id = ""
        self.provider_name = ""
        self.provider_bio = ""
        self.provider_contact_mobile = ""
        self.provider_contact_email = ""
        self.provider_department_ids = []
        self.provider_status = "Active"
        self.provider_error = ""

    @rx.event
    def open_department_modal(self, department: Optional[Department] = None):
        self._clear_department_form()
        if department:
            self.department_form_id = department.id
            self.department_name = department.name
            self.department_description = department.description
        self.show_department_modal = True

    @rx.event
    def close_department_modal(self):
        self.show_department_modal = False
        self._clear_department_form()

    @rx.event
    def save_department(self, form_data: dict):
        self.department_error = ""
        name = form_data.get("name", "").strip()
        description = form_data.get("description", "").strip()
        self.department_name = name
        self.department_description = description
        if not name:
            self.department_error = "Department name is required."
            return
        if not self.department_form_is_edit:
            if any((d.name.lower() == name.lower() for d in self.departments)):
                self.department_error = "A department with this name already exists."
                return
            new_dept = Department(
                id=str(uuid.uuid4()),
                business_id=self.businesses[0].id,
                name=name.strip(),
                description=description.strip(),
            )
            self.departments.append(new_dept)
            yield rx.toast("Department added successfully!")
        else:
            department = self._get_department_by_id(self.department_form_id)
            if department:
                department.name = name
                department.description = description
                yield rx.toast("Department updated successfully!")
        yield ManagementState.close_department_modal()

    @rx.event
    def confirm_delete_department(self, department_id: str):
        providers_in_dept = [
            p for p in self.providers if department_id in p.department_ids
        ]
        if providers_in_dept:
            self.delete_warning_message = f"Cannot delete department. It is assigned to {len(providers_in_dept)} provider(s). Reassign them first."
            self.item_to_delete_id = ""
        else:
            self.delete_warning_message = "Are you sure you want to delete this department? This action cannot be undone."
            self.item_to_delete_id = department_id
        self.delete_item_type = "department"
        self.show_delete_confirmation = True

    @rx.event
    def execute_delete(self):
        if self.item_to_delete_id:
            if self.delete_item_type == "department":
                self.departments = [
                    d for d in self.departments if d.id != self.item_to_delete_id
                ]
                yield rx.toast("Department deleted successfully!")
            elif self.delete_item_type == "provider":
                result = self.archive_provider(self.item_to_delete_id)
                if result:
                    yield rx.toast(result, duration=5000)
                else:
                    yield rx.toast("Provider archived successfully!")
        else:
            yield rx.toast(self.delete_warning_message, duration=5000)
        self.show_delete_confirmation = False
        self.item_to_delete_id = ""
        self.delete_item_type = ""
        self.delete_warning_message = ""

    @rx.event
    def open_provider_modal(self, provider: Optional[Provider] = None):
        self._clear_provider_form()
        if provider:
            self.provider_form_id = provider.id
            self.provider_name = provider.name
            self.provider_bio = provider.bio
            self.provider_contact_mobile = provider.contact_mobile
            self.provider_contact_email = provider.contact_email
            self.provider_department_ids = provider.department_ids
            self.provider_status = provider.status
        self.show_provider_modal = True

    @rx.event
    def close_provider_modal(self):
        self.show_provider_modal = False
        self._clear_provider_form()

    @rx.event
    def save_provider(self, form_data: dict):
        self.provider_error = ""
        name = form_data.get("name", "").strip()
        bio = form_data.get("bio", "").strip()
        contact_mobile = form_data.get("contact_mobile", "").strip()
        contact_email = form_data.get("contact_email", "").strip()
        self.provider_name = name
        self.provider_bio = bio
        self.provider_contact_mobile = contact_mobile
        self.provider_contact_email = contact_email
        if not name:
            self.provider_error = "Provider name is required."
            return
        if not self.provider_department_ids:
            self.provider_error = "At least one department must be selected."
            return
        if not self.provider_form_is_edit:
            new_provider = Provider(
                id=str(uuid.uuid4()),
                name=name,
                department_ids=self.provider_department_ids,
                status=self.provider_status,
                bio=bio,
                contact_mobile=contact_mobile,
                contact_email=contact_email,
            )
            self.providers.append(new_provider)
            yield rx.toast("Provider added successfully!")
        else:
            provider = self._get_provider_by_id(self.provider_form_id)
            if provider:
                provider.name = name
                provider.department_ids = self.provider_department_ids
                provider.status = self.provider_status
                provider.bio = bio
                provider.contact_mobile = contact_mobile
                provider.contact_email = contact_email
                yield rx.toast("Provider updated successfully!")
        yield ManagementState.close_provider_modal()

    @rx.event
    def confirm_archive_provider(self, provider_id: str):
        provider = self._get_provider_by_id(provider_id)
        if not provider:
            return
        has_active_appointments = any(
            (
                a.provider_id == provider_id and a.status in ["Pending", "Confirmed"]
                for a in self.appointments
            )
        )
        if has_active_appointments:
            self.delete_warning_message = (
                "Cannot archive provider with pending or confirmed appointments."
            )
            self.item_to_delete_id = ""
        else:
            self.delete_warning_message = "Are you sure you want to archive this provider? This will set their status to 'Archived'."
            self.item_to_delete_id = provider_id
        self.delete_item_type = "provider"
        self.show_delete_confirmation = True

    @rx.event
    def change_provider_status(self, provider_id: str, new_status: str):
        provider = self._get_provider_by_id(provider_id)
        if provider:
            provider.status = new_status
            yield rx.toast(f"Provider status changed to {new_status}")

    @rx.event
    def toggle_provider_department(self, department_id: str, checked: bool):
        department_id_str = str(department_id)
        if checked:
            if department_id_str not in self.provider_department_ids:
                self.provider_department_ids.append(department_id_str)
        elif department_id_str in self.provider_department_ids:
            self.provider_department_ids.remove(department_id_str)