from django.db import models
from django.contrib.auth.models import AbstractUser


from django.db import models
from django.contrib.auth.models import AbstractUser


class Location(models.Model):
    country = models.CharField(
        max_length=100,
        default="India"
    )

    state = models.CharField(
        max_length=100
    )

    district = models.CharField(
        max_length=100
    )

    city = models.CharField(
        max_length=100
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["state", "district", "city"]
        unique_together = ("state", "district", "city")

    def __str__(self):
        return f"{self.city}, {self.district}, {self.state}"


class User(AbstractUser):

    # username = None
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )
    ROLE_CHOICES = (
        ('tourist', 'Tourist'),
        ('guide', 'Guide'),
        ('admin' , 'Admin'),
    )
    username = models.CharField(
        max_length=150,
        unique=True
    )

    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=15,
        # blank=True,
        # null=True
    )

    # location = models.CharField(
    #     max_length=255,
    #     blank=True,
    #     null=True
    # )
    
    locations = models.ManyToManyField(
        Location,
        blank=True,
        related_name="guides"
    )
    
    # state = models.CharField(
    #     max_length=100,
    #     blank=True,
    #     null=True
    # )

    # country = models.CharField(
    #     max_length=100,
    #     default="India",
    #     null =True,
    #     blank=True
    # )


    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )
    
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )


    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email




class GuideProfile(models.Model):
    VERIFICATION_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="guide_profile"
    )

    # Guide information
    bio = models.TextField(
        blank=True,
        null=True
    )

    experience_years = models.PositiveIntegerField(
        default=0
    )

    languages = models.CharField(
        max_length=500,
    )

    # Aadhaar / Identity documents
    aadhaar_front = models.ImageField(
        upload_to="guide_documents/aadhaar/"
    )

    aadhaar_back = models.ImageField(
        upload_to="guide_documents/aadhaar/"
    )

    # Other documents
    
    # identity_document = models.FileField(
    #     upload_to="guide_documents/identity/",
    #     blank=True,
    #     null=True
    # )

    certificates = models.FileField(
        upload_to="guide_documents/certificates/",
        blank=True,
        null=True
    )

    # Verification
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_CHOICES,
        default="pending"
    )

    rejection_reason = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Guide Profile - {self.user.email}"











from django.db import models
from django.utils import timezone
from datetime import timedelta
class RegistrationOTP(models.Model):
    email = models.EmailField(unique=True)

    otp = models.CharField(max_length=6)

    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def is_expired(self):
        return timezone.now() > self.expires_at

    def set_expiry(self):
        self.expires_at = timezone.now() + timedelta(minutes=10)