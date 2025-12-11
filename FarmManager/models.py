from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


# --- Base Models for Common Patterns ---
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def all_with_deleted(self):
        return super().get_queryset()

    def deleted(self):
        return super().get_queryset().filter(is_deleted=True)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class BaseChoiceModel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name

    class Meta:
        abstract = True
        ordering = ["name"]


# --- Choice Models ---
class HousingType(BaseChoiceModel):
    pass


class FloorType(BaseChoiceModel):
    pass


class FeedingFrequency(BaseChoiceModel):
    pass


class WaterSource(BaseChoiceModel):
    pass


class BreedType(BaseChoiceModel):
    pass


class GynecologicalStatus(BaseChoiceModel):
    pass


class UdderHealthStatus(BaseChoiceModel):
    pass


class MastitisStatus(BaseChoiceModel):
    pass


class GeneralHealthStatus(BaseChoiceModel):
    pass


# --- Main Models ---
class Farm(SoftDeleteModel):
    FARM_HYGIENE_CHOICES = [(i, str(i)) for i in range(1, 5)]

    farm_id = models.CharField(max_length=50, primary_key=True)
    owner_name = models.CharField(max_length=255)
    address = models.TextField()
    telephone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message=_(
                    "Enter a valid phone number (e.g. +251912345678 or 0912345678)"
                ),
            )
        ],
    )
    location_gps = models.CharField(max_length=255, blank=True, null=True)
    cluster_number = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        db_index=True,  # Add index for faster filtering
        help_text=_("Cluster identifier for grouping farms")
    )
    fertility_camp_no = models.PositiveIntegerField(
        help_text=_("Number of fertility camps")
    )

    # Cow population
    total_number_of_cows = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], help_text=_("Total number of cows")
    )
    number_of_calves = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], help_text=_("Number of calves")
    )
    number_of_milking_cows = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], help_text=_("Number of milking cows")
    )
    total_daily_milk = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text=_("Total daily milk production in liters"),
    )

    # Infrastructure
    type_of_housing = models.ForeignKey(
        HousingType, on_delete=models.PROTECT, related_name="farms"
    )
    type_of_floor = models.ForeignKey(
        FloorType, on_delete=models.PROTECT, related_name="farms"
    )

    # Feeding
    main_feed = models.TextField()
    rate_of_cow_feeding = models.ForeignKey(
        FeedingFrequency, on_delete=models.PROTECT, related_name="farms_feeding"
    )

    # Water
    source_of_water = models.ForeignKey(
        WaterSource, on_delete=models.PROTECT, related_name="farms"
    )
    rate_of_water_giving = models.ForeignKey(
        FeedingFrequency, on_delete=models.PROTECT, related_name="farms_watering"
    )

    # Hygiene and Staff
    farm_hygiene_score = models.PositiveIntegerField(
        choices=FARM_HYGIENE_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
    )
    inseminator = models.ForeignKey(
        "Inseminator",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_farms",
    )
    doctor = models.ForeignKey(
        "Doctor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_farms",
    )

    def __str__(self):
        return f"Farm {self.farm_id} - {self.owner_name}"


class Cow(SoftDeleteModel):
    class Gender(models.TextChoices):
        FEMALE = "F", _("Female")
        MALE = "M", _("Male")

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="cows")
    cow_id = models.CharField(max_length=50)
    breed = models.ForeignKey(BreedType, on_delete=models.PROTECT, related_name="cows")

    # Demographics
    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=Gender.choices)

    # Health Metrics
    parity = models.PositiveIntegerField(
        default=0, help_text=_("Number of times the cow has given birth")
    )
    body_weight = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )
    bcs = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        choices=[
            (x / 2, str(x / 2)) for x in range(2, 11)
        ],  # 1.0 to 5.0 in 0.5 increments
        verbose_name=_("Body Condition Score"),
    )
    gynecological_status = models.ForeignKey(
        GynecologicalStatus, on_delete=models.PROTECT, related_name="cows"
    )

    # Milk Production
    lactation_number = models.PositiveIntegerField(default=0)
    days_in_milk = models.PositiveIntegerField(default=0)
    average_daily_milk = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )

    # Reproduction
    cow_inseminated_before = models.BooleanField(default=False)
    last_date_insemination = models.DateField(null=True, blank=True)
    number_of_inseminations = models.PositiveIntegerField(default=0)
    id_or_breed_bull_used = models.CharField(max_length=100, blank=True)
    last_calving_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("farm", "cow_id")
        ordering = ["farm", "cow_id"]

    def __str__(self):
        return f"Farm {self.farm.farm_id} - Cow {self.cow_id}"

    @property
    def full_id(self):
        return f"{self.farm.farm_id}_{self.cow_id}"


class Reproduction(SoftDeleteModel):
    farm = models.ForeignKey(
        Farm, on_delete=models.CASCADE, related_name="reproductions"
    )
    cow = models.ForeignKey(
        Cow, on_delete=models.CASCADE, related_name="reproductions"
    )

    # Heat Detection
    heat_sign_start = models.DateTimeField(null=True, blank=True)
    heat_sign_end = models.DateTimeField(null=True, blank=True)
    heat_signs_seen = models.TextField(null=True, blank=True)

    # Pregnancy Tracking
    is_cow_pregnant = models.BooleanField(default=False)
    pregnancy_date = models.DateField(null=True, blank=True)
    calving_date = models.DateField(null=True, blank=True)

    # New field to track when heat sign was recorded
    heat_sign_recorded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Reproduction record for {self.cow.cow_id} at {self.heat_sign_recorded_at}"

    class Meta:
        ordering = ["-heat_sign_recorded_at"]  # Order by most recent heat sign records first


class Message(SoftDeleteModel):
    class MessageType(models.TextChoices):
        HEAT_ALERT = "heat_alert", _("Heat Alert")
        HEALTH_ALERT = "health_alert", _("Health Alert")
        VACCINATION_ALERT = "vaccination_alert", _("Vaccination Alert")
        PREGNANCY_UPDATE = "pregnancy_update", _("Pregnancy Update")
        INSEMINATOR_ALERT = "inseminator_alert", _("Inseminator Alert")
        FARMER_ALERT = "farmer_alert", _("Farmer Alert")
        DOCTOR_ALERT = "doctor_alert", _("Doctor Alert")
        DOCTOR_ASSIGNMENT = "doctor_assignment", _("Doctor Assignment")
        INSEMINATOR_ASSIGNMENT = "inseminator_assignment", _("Inseminator Assignment")
        PREGNANCY_CONFIRMATION = "pregnancy_confirmation", _("Pregnancy Confirmation")
        OTHER = "other", _("Other")

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="messages")
    cow = models.ForeignKey(
        Cow, on_delete=models.CASCADE, related_name="messages", null=True, blank=True
    )
    message_text = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=50, choices=MessageType.choices)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Message for Farm {self.farm.farm_id} - Cow {self.cow.cow_id}"

    class Meta:
        ordering = ["-sent_date"]


class StaffMember(SoftDeleteModel):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message=_(
                    "Enter a valid phone number (e.g. +251912345678 or 0912345678)"
                ),
            )
        ],
    )
    address = models.TextField()
    is_active = models.BooleanField(default=True)


class Inseminator(StaffMember):
    def __str__(self):
        return f"{self.name} - {self.phone_number}"

    class Meta:
        ordering = ["name"]


class Doctor(StaffMember):
    license_number = models.CharField(max_length=50, unique=True)
    specialization = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.license_number}"

    class Meta:
        ordering = ["name"]


class FarmerMedicalReport(SoftDeleteModel):
    farm = models.ForeignKey(
        Farm, on_delete=models.CASCADE, related_name="farmer_medical_reports"
    )
    cow = models.ForeignKey(
        Cow, on_delete=models.CASCADE, related_name="farmer_medical_reports"
    )
    sickness_description = models.TextField()
    reported_date = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        Doctor, on_delete=models.SET_NULL, null=True, blank=True
    )
    review_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Medical Report - Farm {self.farm.farm_id} - Cow {self.cow.cow_id}"

    class Meta:
        ordering = ["-reported_date"]


class MedicalAssessment(SoftDeleteModel):
    class SicknessType(models.TextChoices):
        INFECTIOUS = "infectious", _("Infectious Disease")
        NON_INFECTIOUS = "non_infectious", _("Non-Infectious Disease")

    farm = models.ForeignKey(
        Farm, on_delete=models.CASCADE, related_name="medical_assessments"
    )
    cow = models.ForeignKey(
        Cow, on_delete=models.CASCADE, related_name="medical_assessments"
    )
    assessed_by = models.ForeignKey(
        Doctor, on_delete=models.PROTECT, related_name="assessments"
    )
    assessment_date = models.DateTimeField(auto_now_add=True)

    # Health Status
    is_cow_sick = models.BooleanField(default=False)
    sickness_type = models.CharField(
        max_length=20, choices=SicknessType.choices, null=True, blank=True
    )
    general_health = models.ForeignKey(GeneralHealthStatus, on_delete=models.PROTECT)
    udder_health = models.ForeignKey(UdderHealthStatus, on_delete=models.PROTECT)
    mastitis = models.ForeignKey(MastitisStatus, on_delete=models.PROTECT)
    has_lameness = models.BooleanField(default=False, help_text=_("Whether the cow shows signs of lameness"))
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
        ordering = ["-assessment_date"]


class InseminationRecord(SoftDeleteModel):
    farm = models.ForeignKey(
        Farm, on_delete=models.CASCADE, related_name="insemination_records"
    )
    cow = models.ForeignKey(
        Cow, on_delete=models.CASCADE, related_name="insemination_records"
    )
    inseminator = models.ForeignKey(
        Inseminator, on_delete=models.PROTECT, related_name="insemination_records"
    )
    is_inseminated = models.BooleanField(default=False)
    insemination_date = models.DateField(null=True, blank=True, help_text="Actual date when insemination was performed")
    insemination_time = models.TimeField(null=True, blank=True)
    insemination_count = models.IntegerField(default=0)
    lactation_number = models.IntegerField()
    recorded_date = models.DateTimeField(auto_now_add=True, help_text="Date when this record was created in the system")

    def __str__(self):
        return f"Insemination Record - Farm {self.farm.farm_id} - Cow {self.cow.cow_id}"

    class Meta:
        ordering = ["-recorded_date"]
