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
    doctor = models.ForeignKey(
        'Doctor',
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
    cow = models.ForeignKey(
        Cow, 
        on_delete=models.CASCADE, 
        related_name='messages',
        null=True,
        blank=True
    )
    message_text = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=50, choices=[
        ('heat_alert', 'Heat Alert'),
        ('health_alert', 'Health Alert'),
        ('vaccination_alert', 'Vaccination Alert'),
        ('pregnancy_update', 'Pregnancy Update'),
        ('inseminator_alert', 'Inseminator Alert'),
        ('farmer_alert', 'Farmer Alert'),
        ('doctor_alert', 'Doctor Alert'),
        ('doctor_assignment', 'Doctor Assignment'),
        ('inseminator_assignment', 'Inseminator Assignment'),
        ('pregnancy_confirmation', 'Pregnancy Confirmation'),
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

class Doctor(models.Model):
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
    specialization = models.CharField(max_length=255, blank=True)
    license_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.license_number}"

    class Meta:
        ordering = ['name']

class FarmerMedicalReport(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='farmer_medical_reports')
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='farmer_medical_reports')
    sickness_description = models.TextField()
    reported_date = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    review_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Medical Report - Farm {self.farm.farm_id} - Cow {self.cow.cow_id}"

    class Meta:
        ordering = ['-reported_date']

class MedicalAssessment(models.Model):
    SICKNESS_TYPE_CHOICES = [
        ('infectious', 'Infectious Disease'),
        ('non_infectious', 'Non-Infectious Disease')
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='medical_assessments')
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='medical_assessments')
    assessed_by = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='assessments')
    assessment_date = models.DateTimeField(auto_now_add=True)
    
    # Health Status
    is_cow_sick = models.BooleanField(default=False)
    sickness_type = models.CharField(
        max_length=20, 
        choices=SICKNESS_TYPE_CHOICES,
        null=True, 
        blank=True
    )
    general_health = models.ForeignKey(GeneralHealthStatus, on_delete=models.PROTECT)
    udder_health = models.ForeignKey(UdderHealthStatus, on_delete=models.PROTECT)
    mastitis = models.ForeignKey(MastitisStatus, on_delete=models.PROTECT)
    body_condition_score = models.IntegerField()
    reproductive_health = models.TextField()
    metabolic_disease = models.TextField(blank=True)
    
    # Vaccination
    is_cow_vaccinated = models.BooleanField(default=False)
    vaccination_date = models.DateField(null=True, blank=True)
    vaccination_type = models.CharField(max_length=255, blank=True)
    
    # Deworming
    has_deworming = models.BooleanField(default=False)
    deworming_date = models.DateField(null=True, blank=True)
    deworming_type = models.CharField(max_length=255, blank=True)
    
    # Assessment Details
    diagnosis = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    next_assessment_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Medical Assessment - Farm {self.farm.farm_id} - Cow {self.cow.cow_id}"

    class Meta:
        ordering = ['-assessment_date']

class InseminationRecord(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='insemination_records')
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='insemination_records')
    inseminator = models.ForeignKey(Inseminator, on_delete=models.PROTECT, related_name='insemination_records')
    is_inseminated = models.BooleanField(default=False)
    insemination_time = models.TimeField(null=True, blank=True)
    insemination_count = models.IntegerField(default=0)
    lactation_number = models.IntegerField()
    recorded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Insemination Record - Farm {self.farm.farm_id} - Cow {self.cow.cow_id}"

    class Meta:
        ordering = ['-recorded_date']
