from django.db import models

# Create your models here.
# coupons/models.py

from django.db import models
from django.utils import timezone
from decimal import Decimal

from user.models import User
from tourist.models import Tour


class Coupon(models.Model):

    DISCOUNT_TYPE_CHOICES = (
        ('flat', 'Flat Amount'),
        ('percentage', 'Percentage'),
    )

    # Optional → specific tour coupon
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='coupons'
    )

    title = models.CharField(
        max_length=150,
        help_text="Example: Summer Offer"
    )

    code = models.CharField(
        max_length=30,
        unique=True,
        help_text="Example: SUMMER50"
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES
    )

    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="20 = 20% | 500 = ₹500"
    )

    min_booking_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    max_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Only for percentage coupons"
    )

    start_date = models.DateField()

    end_date = models.DateField()

    usage_limit = models.PositiveIntegerField(
        default=0,
        help_text="0 = Unlimited"
    )

    used_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def is_valid(self):

        today = timezone.now().date()

        if not self.is_active:
            print("FAILED ACTIVE")
            return False

        if not (self.start_date <= today <= self.end_date):
            print("FAILED DATE")
            return False

        if self.usage_limit != 0 and self.used_count >= self.usage_limit:
            print("FAILED LIMIT")
            return False

        return True

    def calculate_discount(self, amount):

        if amount < self.min_booking_amount:
            return Decimal("0.00")

        if self.discount_type == 'percentage':

            discount = (
                amount * self.discount_value
            ) / Decimal("100")

            if self.max_discount_amount:
                discount = min(
                    discount,
                    self.max_discount_amount
                )

            return discount

        return min(self.discount_value, amount)

    def __str__(self):
        return f"{self.code}"
    
    
    


class CouponUsage(models.Model):
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    booking = models.ForeignKey(
        'booking.Booking',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    used_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.email} used {self.coupon.code}"