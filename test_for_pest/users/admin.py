from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model, decorators
from django.utils.translation import gettext_lazy as _

from test_for_pest.users.forms import UserAdminChangeForm, UserAdminCreationForm
from .models import Customer, TestOperator, GovernmentOfficial, Doctor, Appointment, TestResult, Statistics, Communication

User = get_user_model()

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://django-allauth.readthedocs.io/en/stable/advanced.html#admin
    admin.site.login = decorators.login_required(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "is_superuser"]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 1
    fields = ('scheduled_time', 'test_operator', 'status')

class TestResultInline(admin.TabularInline):
    model = TestResult
    extra = 1
    fields = ('result', 'disease_tested')

class CommunicationInline(admin.TabularInline):
    model = Communication
    extra = 1
    fields = ('government_official', 'message_content', 'timestamp')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__email', 'phone')
    inlines = [AppointmentInline, CommunicationInline]

class TestOperatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'location')
    search_fields = ('user__email', 'location')
    inlines = [AppointmentInline]

class GovernmentOfficialAdmin(admin.ModelAdmin):
    list_display = ('user', 'region')
    search_fields = ('user__email', 'region')
    inlines = [CommunicationInline]

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization')
    search_fields = ('user__email', 'specialization')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'test_operator', 'scheduled_time', 'status')
    list_filter = ('scheduled_time', 'status')
    inlines = [TestResultInline]

class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('region', 'total_tests', 'positive_results', 'date')
    list_filter = ('region', 'date')

class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'government_official', 'timestamp')
    list_filter = ('timestamp', 'government_official')
    search_fields = ('customer__user__email', 'government_official__user__email')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(TestOperator, TestOperatorAdmin)
admin.site.register(GovernmentOfficial, GovernmentOfficialAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(Communication, CommunicationAdmin)
