from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

# Choice Models
class HousingType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name

class FloorType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name

class FeedingFrequency(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name

class WaterSource(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name

# Farm Model
class Farm(models.Model):
    farm_id = models.CharField(max_length=50, primary_key=True)
    owner_name = models.CharField(max_length=255)
    address = models.TextField()
    telephone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Enter a valid phone number (e.g. +251912345678 or 0912345678)."
        )]
    )
    location_gps = models.CharField(max_length=255, null=True, blank=True)
    fertility_camp_no = models.PositiveIntegerField(
        help_text="Number of fertility camps"
    )
    total_number_of_cows = models.PositiveIntegerField()
    number_of_calves = models.PositiveIntegerField()
    number_of_milking_cow = models.PositiveIntegerField()
    total_daily_milk = models.PositiveIntegerField(
        help_text="Total daily milk production in liters"
    )
    type_of_housing = models.ForeignKey(
        HousingType,
        on_delete=models.PROTECT,
        related_name='farms'
    )
    type_of_floor = models.ForeignKey(
        FloorType,
        on_delete=models.PROTECT,
        related_name='farms'
    )
    main_feed = models.TextField()
    rate_of_cow_feeding = models.ForeignKey(
        FeedingFrequency,
        on_delete=models.PROTECT,
        related_name='farms_feeding'
    )
    source_of_water = models.ForeignKey(
        WaterSource,
        on_delete=models.PROTECT,
        related_name='farms'
    )
    rate_of_water_giving = models.ForeignKey(
        FeedingFrequency,
        on_delete=models.PROTECT,
        related_name='farms_watering'
    )
    farm_hygiene_score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    inseminator = models.ForeignKey(
        'Inseminator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_farms'
    )

    def __str__(self):
        return f"Farm {self.farm_id} - {self.owner_name}"

# Additional choice models for Cow
class BreedType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name

class GynecologicalStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name

# Cow Model
class Cow(models.Model):
    GENDER_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male')
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='cows')
    cow_id = models.CharField(max_length=50)
    breed = models.ForeignKey(
        BreedType,
        on_delete=models.PROTECT,
        related_name='cows'
    )
    age_in_days = models.PositiveIntegerField()
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    parity = models.PositiveIntegerField(
        help_text="Number of times the cow has given birth",
        default=0
    )
    body_weight = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    bcs = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        choices=[(1, '1'), (1.5, '1.5'), (2, '2'), (2.5, '2.5'), 
                (3, '3'), (3.5, '3.5'), (4, '4'), (4.5, '4.5'), (5, '5')],
        verbose_name="Body Condition Score"
    )
    gynecological_status = models.ForeignKey(
        GynecologicalStatus,
        on_delete=models.PROTECT,
        related_name='cows'
    )
    lactation_number = models.PositiveIntegerField(default=0)
    days_in_milk = models.PositiveIntegerField(default=0)
    average_daily_milk = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    cow_inseminated_before = models.BooleanField(default=False)
    last_date_insemination = models.DateField(null=True, blank=True)
    number_of_inseminations = models.PositiveIntegerField(default=0)
    id_or_breed_bull_used = models.CharField(max_length=100, blank=True)
    last_calving_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Farm {self.farm.farm_id} - Cow {self.cow_id}"

    class Meta:
        unique_together = ('farm', 'cow_id')
        ordering = ['farm', 'cow_id']
    # Optional: Method to get a cow's "full ID"
    @property
    def full_id(self):
        return f"{self.farm.farm_id}_{self.cow_id}"

# Choice models for Health
class UdderHealthStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name

class MastitisStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name

class GeneralHealthStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name

# Health Model
class Health(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='health_records')
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='health_records')
    udder_health = models.ForeignKey(
        UdderHealthStatus,
        on_delete=models.PROTECT,
        related_name='health_records'
    )
    mastitis = models.ForeignKey(
        MastitisStatus,
        on_delete=models.PROTECT,
        related_name='health_records'
    )
    general_health = models.ForeignKey(
        GeneralHealthStatus,
        on_delete=models.PROTECT,
        related_name='health_records'
    )
    reproductive_health = models.TextField(blank=True)
    metabolic_health = models.TextField(blank=True)
    is_cow_vaccinated = models.BooleanField(default=False)
    vaccination_date = models.DateField(null=True, blank=True)
    vaccination_type = models.TextField(blank=True)
    has_cow_taken_deworming = models.BooleanField(default=False)
    deworming_date = models.DateField(null=True, blank=True)
    deworming_type = models.TextField(blank=True)

    def __str__(self):
        return f"Health Record - Cow {self.cow.cow_id}"

    class Meta:
        verbose_name_plural = "Health Records"

# Reproduction Model
class Reproduction(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='reproduction_records')
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='reproduction_records')
    is_cow_pregnant = models.BooleanField(default=False)
    heat_sign_start = models.DateTimeField()
    heat_sign_end = models.DateTimeField(null=True, blank=True)
    heat_signs_seen = models.TextField(blank=True)
    pregnancy_date = models.DateField(null=True, blank=True)
    calving_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Reproduction Record - Cow {self.cow.cow_id}"

    class Meta:
        verbose_name_plural = "Reproduction Records"

class Message(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='messages')
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='messages')
    message_text = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=50, choices=[
        ('heat_alert', 'Heat Alert'),
        ('health_alert', 'Health Alert'),
        ('vaccination_alert', 'Vaccination Alert'),
        ('other', 'Other')
    ])
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Message for Farm {self.farm.farm_id} - Cow {self.cow.cow_id}"

    class Meta:
        ordering = ['-sent_date']

class Inseminator(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Enter a valid phone number (e.g. +251912345678 or 0912345678)."
        )]
    )
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

    class Meta:
        ordering = ['name']
