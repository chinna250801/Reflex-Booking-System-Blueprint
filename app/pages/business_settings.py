import reflex as rx
from app.states.management_state import ManagementState


def business_profile_section() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Business Profile", class_name="text-xl font-semibold text-gray-800 mb-4"
        ),
        rx.el.form(
            rx.el.div(
                rx.el.div(
                    rx.el.label("Display Name", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="display_name",
                        default_value=ManagementState.business_display_name,
                        class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg",
                    ),
                    class_name="flex-1",
                ),
                rx.el.div(
                    rx.el.label("Legal Name", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="legal_name",
                        default_value=ManagementState.business_legal_name,
                        class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg",
                    ),
                    class_name="flex-1",
                ),
                class_name="flex gap-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Registration Number", class_name="text-sm font-medium"
                    ),
                    rx.el.input(
                        name="registration_number",
                        default_value=ManagementState.business_registration_number,
                        class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg",
                    ),
                    class_name="flex-1",
                ),
                rx.el.div(
                    rx.el.label("GSTN", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="gstn",
                        default_value=ManagementState.business_gstn,
                        class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg",
                    ),
                    class_name="flex-1",
                ),
                class_name="flex gap-6",
            ),
            rx.el.div(
                rx.el.label("Address", class_name="text-sm font-medium"),
                rx.el.input(
                    name="address",
                    default_value=ManagementState.business_address,
                    class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label("Contact Mobile", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="contact_mobile",
                        default_value=ManagementState.business_contact_mobile,
                        class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg",
                    ),
                    class_name="flex-1",
                ),
                rx.el.div(
                    rx.el.label("Contact Email", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="contact_email",
                        type="email",
                        default_value=ManagementState.business_contact_email,
                        class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg",
                    ),
                    class_name="flex-1",
                ),
                class_name="flex gap-6",
            ),
            rx.el.div(
                rx.el.button(
                    "Save Changes",
                    type="submit",
                    class_name="px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors",
                ),
                class_name="flex justify-end mt-4",
            ),
            class_name="space-y-4",
            on_submit=ManagementState.save_business_settings,
        ),
        class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
    )


def business_logo_section() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Business Logo", class_name="text-xl font-semibold text-gray-800 mb-4"
        ),
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=rx.get_upload_url(ManagementState.business_logo_url),
                    class_name="h-24 w-24 rounded-lg object-cover border border-gray-200",
                ),
                rx.upload.root(
                    rx.el.button(
                        "Change Logo", class_name="text-sm text-emerald-600 font-medium"
                    ),
                    id="logo-upload",
                    on_drop=ManagementState.handle_logo_upload,
                ),
            ),
            class_name="flex items-center gap-6",
        ),
        class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm mt-6",
    )


def business_settings_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Business Settings", class_name="text-2xl font-bold text-gray-900 mb-6"
        ),
        business_profile_section(),
        business_logo_section(),
        class_name="max-w-[1200px] w-full mx-auto",
        on_mount=ManagementState.on_business_settings_load,
    )