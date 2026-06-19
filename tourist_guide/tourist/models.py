from django.db import models

# Create your models here.


# models.py


# tours/models.py

from django.db import models
from django.conf import settings
from django.utils.text import slugify


# =========================
# TOUR CATEGORY
# =========================

class TourCategory(models.Model):

    name = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to='tour_categories/'
    )

    is_active = models.BooleanField(default=True)
    slot_position = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['slot_position']

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name



# =========================
# TOUR HIGHLIGHTS
# =========================

class TourHighlight(models.Model):

    # tour = models.ForeignKey(
    #     Tour,
    #     on_delete=models.CASCADE,
    #     related_name="highlights"
    # )

    title = models.CharField(
        max_length=255
    )
    is_active = models.BooleanField(
        default=True
    )

    slot_position = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['slot_position']
    def __str__(self):

        return self.title


# =========================
# TOUR INCLUDES
# =========================

class TourInclude(models.Model):

    # tour = models.ForeignKey(
    #     Tour,
    #     on_delete=models.CASCADE,
    #     related_name="includes"
    # )

    title = models.CharField(
        max_length=255
    )
    
    is_active = models.BooleanField(
        default=True
    )

    slot_position = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['slot_position']

    def __str__(self):

        return self.title


# =========================
# TOUR EXCLUDES
# =========================

class TourExclude(models.Model):

    # tour = models.ForeignKey(Tour,on_delete=models.CASCADE,related_name="excludes")

    title = models.CharField(
        max_length=255
    )
    is_active = models.BooleanField(
        default=True
    )

    slot_position = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['slot_position']

    def __str__(self):

        return self.title


# =========================
# IMPORTANT INFORMATION
# =========================

class ImportantInformation(models.Model):

    # tour = models.ForeignKey(
    #     Tour,
    #     on_delete=models.CASCADE,
    #     related_name="important_information"
    # )

    title = models.CharField(
        max_length=255
    )
    is_active = models.BooleanField(
        default=True
    )

    slot_position = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['slot_position']

    def __str__(self):

        return self.title




# =========================
# AMENITIES
# =========================

class Amenity(models.Model):

    name = models.CharField(
        max_length=100
    )

    icon_class = models.CharField(
        max_length=100
    )
    
    is_active = models.BooleanField(
        default=True
    )

    slot_position = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['slot_position']

    def __str__(self):

        return self.name


# =========================
# TOUR AMENITIES
# =========================

# class TourAmenity(models.Model):

#     tour = models.ForeignKey(
#         Tour,
#         on_delete=models.CASCADE,
#         related_name="tour_amenities"
#     )

#     amenity = models.ForeignKey(
#         Amenity,
#         on_delete=models.CASCADE
#     )
#     is_active = models.BooleanField(
#         default=True
#     )

#     slot_position = models.PositiveIntegerField(
#         default=0
#     )

#     class Meta:
#         ordering = ['slot_position']

#     def __str__(self):

#         return (
#             f"{self.tour.title} - "
#             f"{self.amenity.name}"
#         )



# =========================
# TOUR
# =========================

class Tour(models.Model):

    TOUR_TYPE_CHOICES = (
        ('private', 'Private'),
        ('group', 'Group'),
    )

    # guide = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="guide_tours" ,null=True ,blank=True)
    category = models.ForeignKey( TourCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="tours")

    title = models.CharField(
        max_length=255
    )

    slug = models.SlugField(unique=True,blank=True)

    short_description = models.TextField()

    full_description = models.TextField()

    city = models.CharField(max_length=100)

    state = models.CharField( max_length=100)

    country = models.CharField( max_length=100, default="India")

    address = models.TextField( blank=True, null=True)

    meeting_point = models.TextField(blank=True,null=True)

    duration = models.CharField(  max_length=100,  help_text="Example: 3.5 Hours")

    language = models.CharField(  max_length=100,  default="English")

    tour_type = models.CharField(max_length=20,choices=TOUR_TYPE_CHOICES,default='group')

    max_people = models.PositiveIntegerField( default=10)

    min_age = models.PositiveIntegerField( default=1)

    # price = models.DecimalField( max_digits=10, decimal_places=2 )

    # offer_price = models.DecimalField( max_digits=10,decimal_places=2,null=True,blank=True)

    free_cancellation = models.BooleanField( default=True)

    instant_confirmation = models.BooleanField( default=True)

    pickup_available = models.BooleanField(default=False)

    wheelchair_accessible = models.BooleanField(default=False)

    featured = models.BooleanField( default=False)



    slot_position = models.PositiveIntegerField(
        default=0
    )
    
    includes = models.ManyToManyField(
        TourInclude,
        blank=True,
        related_name="tours"
    )

    excludes = models.ManyToManyField(
        TourExclude,
        blank=True,
        related_name="tours"
    )

    highlights = models.ManyToManyField(
        TourHighlight,
        blank=True,
        related_name="tours"
    )

    important_information = models.ManyToManyField(
        ImportantInformation,
        blank=True,
        related_name="tours"
    )

    amenities = models.ManyToManyField(
        Amenity,
        blank=True,
        related_name="tours"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField( auto_now=True)

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    # @property
    # def final_price(self):

    #     return self.offer_price or self.price
    
    
    @property
    def final_price(self):

        adult_price = self.pricing.filter(
            person_type="adult",
            is_active=True
        ).first()

        if adult_price:

            return adult_price.price

        return 0
    
    @property
    def adult_price(self):

        price = self.pricing.filter(
            person_type="adult",
            is_active=True
        ).first()

        return price.price if price else 0


    @property
    def child_price(self):

        price = self.pricing.filter(
            person_type="child",
            is_active=True
        ).first()

        return price.price if price else 0


    @property
    def infant_price(self):

        price = self.pricing.filter(
            person_type="infant",
            is_active=True
        ).first()

        return price.price if price else 0

    def __str__(self):

        return self.title


# =========================
# TOUR IMAGES
# =========================

class TourImage(models.Model):

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to='tour_images/'
    )

    is_primary = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.tour.title


# =========================
# TOUR SCHEDULE
# =========================

class TourSchedule(models.Model):

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="schedules"
    )

    start_time = models.TimeField()

    # end_time = models.TimeField()

    available_slots = models.PositiveIntegerField(
        default=10
    )

    is_active = models.BooleanField(
        default=True
    )
    
    slot_position = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['slot_position']



    def __str__(self):

        return (
            f"{self.tour.title} - "
            f"{self.start_time}"
        )
        

# tourist/models.py

class TourPricing(models.Model):

    PERSON_TYPE_CHOICES = [

        ("adult", "Adult"),

        ("child", "Child"),

        ("infant", "Infant"),
    ]

    tour = models.ForeignKey(

        Tour,

        on_delete=models.CASCADE,

        related_name="pricing"
    )

    person_type = models.CharField(

        max_length=20,

        choices=PERSON_TYPE_CHOICES
    )

    price = models.DecimalField(

        max_digits=10,

        decimal_places=2
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):

        return (
            f"{self.tour.title} - "
            f"{self.person_type}"
        )
