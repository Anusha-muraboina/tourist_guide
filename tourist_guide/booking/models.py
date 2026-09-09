from django.db import models

# Create your models here.


# bookings/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse
from decimal import Decimal
from datetime import timedelta, date
from django.db import transaction
import random
import string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from tourist.models import Tour
from coupon.models import Coupon
from user.models import User

from tourist.models import TourPricing
# =========================
# TOUR BOOKING
# =========================
class Booking(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ("on_process", "On Process"),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('pay_at_location', 'Pay At Location'),
        ('partial_payment', 'Pay 30% Advance'),
        ('full_payment', 'Full Payment'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    
    

    booking_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    # =========================
    # TOUR + USER
    # =========================

    tour = models.ForeignKey(  Tour,  on_delete=models.CASCADE,  related_name="bookings")

    # user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="guide_bookings", limit_choices_to={ "role": "guide" } )
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings")
    guide = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="tour_guide_bookings", limit_choices_to={"role": "guide"})


    guide_status = models.CharField(
    max_length=20,
    choices=[
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
    ],
    default="pending",
)
    
    guide_attempt = models.PositiveIntegerField(default=0)
    
    declined_guides = models.JSONField(
    default=list,
    blank=True,
    )
    # =========================
    # GUEST DETAILS
    # =========================
    guest_name = models.CharField(max_length=200)

    guest_email = models.EmailField()

    guest_phone = models.CharField(max_length=15)

    # =========================
    # TRAVELLERS
    # =========================

    # adults = models.PositiveIntegerField(default=1)

    # children = models.PositiveIntegerField(default=0)
    # infants = models.PositiveIntegerField(default=0)

    pricing = models.ForeignKey(
        TourPricing,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings"
        
    )


    group_members = models.PositiveIntegerField(
        default=1
    )
    # =========================


    # TOUR DATE & TIME
    # =========================

    tour_date = models.DateField()

    tour_time = models.TimeField( null=True, blank=True)

    special_requests = models.TextField(  blank=True,  null=True)

    # =========================
    # PRICE
    # =========================

    sub_total = models.DecimalField( max_digits=10, decimal_places=2)

    discount_amount = models.DecimalField( max_digits=10, decimal_places=2, default=Decimal("0.00"))

    tax_amount = models.DecimalField( max_digits=10, decimal_places=2, default=Decimal("0.00") )

    total_amount = models.DecimalField(  max_digits=10,  decimal_places=2)

    # =========================
    # COUPON
    # =========================

    coupon_applied = models.ForeignKey(  Coupon,  on_delete=models.SET_NULL,  null=True, blank=True)

    # =========================
    # PAYMENT
    # =========================

    payment_method = models.CharField( max_length=30, choices=PAYMENT_METHOD_CHOICES)

    payment_status = models.CharField(  max_length=20,  choices=PAYMENT_STATUS_CHOICES,  default='pending')

    payment_id = models.CharField( max_length=100, blank=True, null=True)

    transaction_id = models.CharField( max_length=100, blank=True, null=True)


    razorpay_order_id = models.CharField(
            max_length=100,
            blank=True,
            null=True
        )

    razorpay_signature = models.CharField(
            max_length=255,
            blank=True,
            null=True
        )

    # =========================
    # STATUS
    # =========================
    

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    cancelled_at = models.DateTimeField(
        null=True,
        blank=True
    )

    cancelled_by = models.CharField(
        max_length=20,
        choices=[
            ("user", "User"),
            ("admin", "Admin"),
            ("guide", "Guide"),
        ],
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    
    verification_code = models.CharField(
    max_length=6,
    blank=True,
    null=True,
    editable=False
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']


    # def save(self, *args, **kwargs):

    #     is_new = self.pk is None

    #     old_status = None

    #     if not is_new:
    #         old_status = (
    #             Booking.objects
    #             .get(pk=self.pk)
    #             .status
    #         )

    #     if not self.booking_id:

    #         while True:

    #             random_id = ''.join(
    #                 random.choices(
    #                     string.digits,
    #                     k=8
    #                 )
    #             )

    #             booking_id = f"TG{random_id}"

    #             if not Booking.objects.filter(
    #                 booking_id=booking_id
    #             ).exists():
    #                 break

    #         self.booking_id = booking_id
            
    #         # Generate 6-digit verification code
    #     if is_new and not self.verification_code:
    #         self.verification_code = ''.join(
    #             random.choices(string.digits, k=6)
    #         )
            
    #     if is_new:

    #         if self.payment_method == "pay_at_location":

    #             self.payment_status = "pending"
    #             self.status = "confirmed"

    #         elif self.payment_method == "partial_payment":

    #             self.payment_status = "partial"
    #             self.status = "confirmed"

    #         elif self.payment_method == "full_payment":

    #             self.payment_status = "paid"
    #             self.status = "confirmed"

    #     super().save(*args, **kwargs)

    #     if is_new:

    #         transaction.on_commit(
    #             lambda:
    #             self.send_booking_email(
    #                 "confirmed"
    #             )
    #         )

    #     elif old_status != self.status:

    #         transaction.on_commit(
    #             lambda:
    #             self.send_booking_email(
    #                 self.status
    #             )
    #         )
    
    
    
    # def save(self, *args, **kwargs):

    #     is_new = self.pk is None

    #     old_status = None

    #     if not is_new:
    #         old_status = (
    #             Booking.objects
    #             .get(pk=self.pk)
    #             .status
    #         )

    #     # Generate Booking ID
    #     if not self.booking_id:

    #         while True:

    #             random_id = ''.join(
    #                 random.choices(
    #                     string.digits,
    #                     k=8
    #                 )
    #             )

    #             booking_id = f"TG{random_id}"

    #             if not Booking.objects.filter(
    #                 booking_id=booking_id
    #             ).exists():
    #                 break

    #         self.booking_id = booking_id

    #     # Generate 6-digit verification code
    #     if is_new and not self.verification_code:

    #         self.verification_code = ''.join(
    #             random.choices(
    #                 string.digits,
    #                 k=6
    #             )
    #         )

    #     # Set initial payment/status
        
    #     if is_new:

    #         if self.payment_method == "pay_at_location":

    #             self.payment_status = "pending"
    #             self.status = "confirmed"

    #         elif self.payment_method == "partial_payment":

    #             self.payment_status = "partial"
    #             self.status = "confirmed"

    #         elif self.payment_method == "full_payment":

    #             self.payment_status = "paid"
    #             self.status = "confirmed"

    #     # Save booking.                                     
        
        
        
           
    #     super().save(*args, **kwargs)
                  

    #     # Send confirmation email for new booking
    #     if is_new:

    #         transaction.on_commit(
    #             lambda: self.send_booking_email(
    #                 "confirmed"
    #             )
    #         )

    #     # Send email when status changes
    #     elif old_status != self.status:

    #         # Don't send an email for on_process
    #         # unless you have an on_process email template
    #         if self.status != "on_process":

    #             transaction.on_commit(
    #                 lambda: self.send_booking_email(
    #                     self.status
    #                 )
    #             )
    
    
    def save(self, *args, **kwargs):

        is_new = self.pk is None
        old_status = None

        # Get previous status before updating
        if not is_new:
            old_status = (
                Booking.objects
                .get(pk=self.pk)
                .status
            )

        # =========================
        # GENERATE BOOKING ID
        # =========================
        if not self.booking_id:

            while True:

                random_id = ''.join(
                    random.choices(
                        string.digits,
                        k=8
                    )
                )

                booking_id = f"TG{random_id}"

                if not Booking.objects.filter(
                    booking_id=booking_id
                ).exists():
                    break

            self.booking_id = booking_id

        # =========================
        # GENERATE VERIFICATION CODE
        # =========================
        if is_new and not self.verification_code:

            self.verification_code = ''.join(
                random.choices(
                    string.digits,
                    k=6
                )
            )

        # =========================
        # NEW BOOKING
        # =========================
        if is_new:

            # IMPORTANT:
            # New booking MUST remain pending
            self.status = "pending"

            # Payment status depends on payment method
            if self.payment_method == "pay_at_location":

                self.payment_status = "pending"

            elif self.payment_method == "partial_payment":

                self.payment_status = "partial"

            elif self.payment_method == "full_payment":

                self.payment_status = "paid"

        # =========================
        # SAVE
        # =========================
        super().save(*args, **kwargs)

        # =========================
        # NEW BOOKING EMAIL
        # =========================
        if is_new:

            transaction.on_commit(
                lambda: self.send_booking_email(
                    "pending"
                )
            )

        # =========================
        # STATUS CHANGE EMAIL
        # =========================
        elif old_status != self.status:

            # Don't send email for on_process
            if self.status != "on_process":

                transaction.on_commit(
                    lambda: self.send_booking_email(
                        self.status
                    )
                )

    # =========================
    # ADVANCE PAYMENT
    # =========================
    
    
    # =========================
    # FIND NEXT GUIDE
    # =========================

    def get_next_guide(self):
        """
        Return the next active guide who has not already
        declined this booking.
        """

        from django.contrib.auth import get_user_model

        User = get_user_model()

        declined_ids = self.declined_guides or []

        guides = (
            User.objects
            .filter(
                role="guide",
                is_active=True,
            )
            .exclude(
                id__in=declined_ids
            )
            .exclude(
                id=self.guide_id
            )
            .order_by("id")
        )

        return guides.first()

    @property
    def advance_amount(self):

        if self.payment_method == "partial_payment":

            return (
                self.total_amount * Decimal("0.30")
            ).quantize(Decimal("0.01"))

        elif self.payment_method == "full_payment":

            return self.total_amount

        return Decimal("0.00")

    # =========================
    # REMAINING AMOUNT
    # =========================

    @property
    def remaining_amount(self):

        return (
            self.total_amount -
            self.advance_amount
        )
        
    def __str__(self):

        return (
            f"{self.booking_id} - "
            f"{self.guest_name}"
        )
        
        
    def cancel_booking(
        self,
        user=None,
        reason=None,
        comment=None
    ):
        print("BEFORE:", self.status)

        self.status = "cancelled"
        self.cancelled_at = timezone.now()
        self.cancelled_by = "user"

        if self.payment_status in ["paid", "partial"]:
            self.payment_status = "failed"

        self.save()

        print("AFTER:", self.status)

        BookingCancelComment.objects.create(
            user=user,
            booking=self,
            reason=reason,
            comment=comment or ""
        )
        
    def send_booking_email(self, email_type,request=None):
        """
        email_type:
        pending / confirmed / cancelled / completed
        """

        templates = {
            "pending": {
                "user": "emails/booking_pending_user.html",
                "admin": "emails/booking_pending_user.html",
                "subject_user": "Booking Received – Awaiting Confirmation",
                "subject_admin": f"New Pending Booking - {self.booking_id}",
            },
            "confirmed": {
                "user": "emails/user_booking_email.html",
                "admin": "emails/admin_booking_email.html",
                "subject_user": "✅ Booking Confirmed – Tourist guide",
                "subject_admin": f"Booking Confirmed - {self.booking_id}",
            },
            "cancelled": {
                "user": "emails/booking_cancelled_user.html",
                "admin": "emails/booking_cancelled_user.html",
                "subject_user": "❌ Booking Cancelled",
                "subject_admin": f"Booking Cancelled - {self.booking_id}",
            },
            "completed": {
                "user": "emails/booking_completed_admin.html",
                "admin": "emails/booking_completed_user.html",
                "subject_user": "🎉 Stay Completed – Thank You!",
                "subject_admin": f"Stay Completed - {self.booking_id}",
            }
        }

        config = templates[email_type]

        # context = {"booking": self}
        ####################################
        # ⭐ Generate Invoice URL
        ####################################

        invoice_url = None


        try:
            invoice_path = reverse("view_invoice", args=[self.booking_id])
            invoice_url = f"http://127.0.0.1:8000{invoice_path}"   # change manually when needed
        except:
            invoice_url = None

        context = {
            "booking": self,
            "invoice_url": invoice_url
        }
        # USER EMAIL
        user_html = render_to_string(config["user"], context)

        user_email = EmailMultiAlternatives(
            subject=config["subject_user"],
            body="Booking update",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.guest_email],
        )

        user_email.attach_alternative(user_html, "text/html")
        user_email.send()

        # ADMIN EMAIL
        admin_html = render_to_string(config["admin"], context)

        admin_email = EmailMultiAlternatives(
            subject=config["subject_admin"],
            body="Booking update",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
        )

        admin_email.attach_alternative(admin_html, "text/html")
        admin_email.send()

    # ================= SAVE =================

    # def save(self, *args, **kwargs):

    #     is_new = self.pk is None
    #     old_status = None
        
    #     if not is_new:
    #         old_status = Booking.objects.get(pk=self.pk).status
            
    #     if not self.booking_id:
    #         self.booking_id = "FHH" + ''.join(random.choices(string.digits, k=8))
    #     super().save(*args, **kwargs)
    

# =========================
# BLOCKED TOUR DATE
# =========================

class BlockedTourDate(models.Model):

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="blocked_dates"
    )

    blocked_date = models.DateField()

    reason = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):

        if self.blocked_date < date.today():

            raise ValidationError(
                "Cannot block past dates"
            )

    def __str__(self):

        return (
            f"{self.tour.title} - "
            f"{self.blocked_date}"
        )


# =========================
# TOUR PAYMENT POLICY
# =========================

class TourPaymentPolicy(models.Model):

    tour = models.OneToOneField(
        Tour,
        on_delete=models.CASCADE,
        related_name="payment_policy"
    )

    allow_pay_at_location = models.BooleanField(
        default=True
    )

    allow_partial_payment = models.BooleanField(
        default=True
    )

    allow_full_payment = models.BooleanField(
        default=True
    )

    def __str__(self):

        return self.tour.title


# =========================
# INVOICE
# =========================

class Invoice(models.Model):

    invoice_id = models.CharField(max_length=50,unique=True )

    invoice_date = models.DateField(  auto_now_add=True)

    booking = models.OneToOneField( Booking, on_delete=models.CASCADE,  related_name="invoice")

    is_active = models.BooleanField(
        default=True
    )

    def save(self, *args, **kwargs):

        if not self.invoice_id:

            self.invoice_id = (
                "INV-" +
                ''.join(
                    random.choices(
                        string.digits,
                        k=10
                    )
                )
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.invoice_id


# =========================
# CANCEL REASON
# =========================

class CancelReason(models.Model):

    reason = models.CharField(
        max_length=255
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):

        return self.reason


# =========================
# BOOKING CANCEL COMMENT
# =========================

class BookingCancelComment(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="cancel_comments"
    )

    reason = models.ForeignKey(
        CancelReason,
        on_delete=models.SET_NULL,
        null=True
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"Cancel - "
            f"{self.booking.booking_id}"
        )