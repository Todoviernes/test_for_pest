from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models

from test_for_pest.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Test for Pest.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
                               
                               
class TestOperator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='test_operator_profile')
    location = models.CharField(max_length=100)
    
    
class GovernmentOfficial(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='government_official_profile')
    region = models.CharField(max_length=100)
    
    
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100)
    
    
class Appointment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='appointments')
    test_operator = models.ForeignKey(TestOperator, on_delete=models.CASCADE, related_name='operated_appointments')
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=50)
    
    
class TestResult(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='test_results')
    result = models.CharField(max_length=50)  # Consider using choices for predefined results
    disease_tested = models.CharField(max_length=100)


class Statistics(models.Model):
    region = models.CharField(max_length=100)
    total_tests = models.IntegerField()
    positive_results = models.IntegerField()
    date = models.DateField()  # Represents the date for these statistics


class Communication(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='communications')
    government_official = models.ForeignKey(GovernmentOfficial, on_delete=models.CASCADE, related_name='sent_communications')
    message_content = models.TextField()
    timestamp = models.DateTimeField()
