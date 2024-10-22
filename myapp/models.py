from django.db import models
from multiselectfield import MultiSelectField


class Farm(models.Model):
    # Basic Information
    farm_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    owner_name = models.CharField(max_length=100)
    address = models.TextField()
    telephone = models.CharField(max_length=15)
    gps_location = models.CharField(max_length=255, null=True, blank=True)
    fcc_no = models.CharField(max_length=50, null=True, blank=True)  # Fertility control camp number
    
    # Animal Information
    herd_size = models.IntegerField()
    calves = models.IntegerField()
    heifers = models.IntegerField()  # Number of young female cows above 12 months of age
    milking_cows = models.IntegerField()
    tdm = models.FloatField(help_text="Total Daily Milk produced by the farm in liters")

    # Housing Information
    HOUSING_CHOICES = [
        ('free_stall', 'Free Stall'),
        ('tie_stall', 'Tie Stall'),
        ('traditional', 'Traditional')
    ]
    housing_type = models.CharField(max_length=20, choices=HOUSING_CHOICES)

    # Floor Information
    FLOOR_CHOICES = [
        ('concrete', 'Concrete'),
        ('stone', 'Stone'),
        ('soil', 'Soil'),
        ('mat_bedding', 'Mat or Other Bedding')
    ]
    floor_type = models.CharField(max_length=20, choices=FLOOR_CHOICES)

    # Feed/Feeding Information
    feed_given = models.TextField(help_text="Main feed given to the cows")
    feeding_frequency = models.CharField(max_length=50, help_text="e.g. Once/day, twice/day, three times/day")

    # Watering Information
    watering_frequency = models.CharField(max_length=50, help_text="e.g. Once/day, twice/day, three times/day")
    
    # Hygiene Information
    farm_hygiene_score = models.IntegerField(help_text="Farm hygiene score from 1 to 4")

    def __str__(self):
        return f"Farm of {self.owner_name}"

class Animal(models.Model):
    # Farm to which the cow belongs
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)

    # Predefined Choices for Fields
    SEX_CHOICES = [
        ('milking', 'Milking Cow'),
        ('bull', 'Bull'),
    ]

    BREED_CHOICES = [
        ('hf', 'HF'),
        ('zebu', 'Zebu'),
        ('hf_zebu', 'HF*Zebu Cross'),
        ('other', 'Other'),
    ]

    PD_STATUS_CHOICES = [
        ('pregnant', 'Pregnant'),
        ('non_pregnant', 'Non-pregnant'),
        ('unknown', 'Unknown'),
    ]

    BCS_CHOICES = [
        (1.0, '1.0'), (1.5, '1.5'), (2.0, '2.0'), (2.5, '2.5'),
        (3.0, '3.0'), (3.5, '3.5'), (4.0, '4.0'), (4.5, '4.5'),
        (5.0, '5.0')
    ]

    GYN_STATUS_CHOICES = [
        ('estrus', 'Estrus'),
        ('ai', 'AI'),
        ('pregnant', 'Pregnant'),
        ('abortion', 'Abortion'),
        ('fresh', 'Fresh'),
    ]

    HEAT_SIGN_CHOICES = [
        ('bellowing', 'Bellowing'),
        ('restlessness', 'Restlessness'),
        ('off_feed', 'Off Feed'),
        ('vaginal_discharge', 'Vaginal Discharge'),
        ('mounting_other_cows', 'Mounting Other Cows'),
        ('standing_to_be_mounted', 'Standing to be Mounted'),
        ('head_butting_others', 'Head Butting Others'),
        ('chin_resting', 'Chin Resting'),
    ]

    METABOLIC_DISEASE_CHOICES = [
        ('hypocalcemia', 'Hypocalcemia'),
        ('vit_a_deficiency', 'Vitamin A Deficiency'),
        ('mg_deficiency', 'Magnesium Deficiency'),
        ('ketosis', 'Ketosis'),
        ('acidosis', 'Acidosis'),
    ]

    MASTITIS_CHOICES = [
        ('negative', 'Negative'),
        ('clinical_mastitis', 'Clinical Mastitis'),
        ('cmt_positive', 'CMT +'),
        ('cmt_double_positive', 'CMT ++'),
        ('cmt_triple_positive', 'CMT +++')
    ]

    UDDER_HEALTH_CHOICES = [
        ('4qt_normal', '4qt normal'),
        ('3qt_normal', '3qt normal'),
        ('2qt_normal', '2qt normal'),
        ('1qt_normal', '1qt normal'),
    ]

    CONCEPTION_RATE_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
    ]

    # Animal Information
    cow_id = models.CharField(max_length=50, unique=True)  # ID or number for the cow
    breed = models.CharField(max_length=50, choices=BREED_CHOICES)  # Breed information
    age_months = models.IntegerField()  # Age in months
    sex = models.CharField(max_length=20, choices=SEX_CHOICES)  # Male/Female
    parity = models.IntegerField()  # Number of pregnancies (0-8)
    body_weight = models.FloatField()  # Body weight in kg
    bcs = models.FloatField(choices=BCS_CHOICES)  # Body Condition Score (1 to 5 scale)
    gyn_status = models.CharField(max_length=20, choices=GYN_STATUS_CHOICES)  # Gynecological status
    
    # Pregnancy and Reproductive Information
    pd_status = models.CharField(max_length=20, choices=PD_STATUS_CHOICES)  # Pregnancy status
    days_to_calving = models.IntegerField(null=True, blank=True)  # Days until calving if pregnant
    date_of_calving = models.DateField(null=True, blank=True)  # Date of calving (if applicable)
    lactation_no = models.IntegerField()  # Lactation number (1-7)
    dim = models.IntegerField()  # Number of days in milk
    dmy = models.FloatField()  # Average daily milk yield after calving
    dalc = models.IntegerField()  # Days after last calving

    # Fertility and Heat Signs
    heat_signs = MultiSelectField(choices=HEAT_SIGN_CHOICES, max_length=200)  # Multi-select for heat signs
    fertility_window_start = models.DateTimeField(null=True, blank=True)  # Fertility window start
    fertility_window_end = models.DateTimeField(null=True, blank=True)  # Fertility window end
    conception_rate = models.CharField(max_length=20, choices=CONCEPTION_RATE_CHOICES, null=True, blank=True)

    # Health Information
    udder_health = models.CharField(max_length=255, choices=UDDER_HEALTH_CHOICES)  # Udder health choices
    mastitis = models.CharField(max_length=255, choices=MASTITIS_CHOICES)  # Mastitis status
    general_health = models.CharField(max_length=255)  # General health (Normal, Sick, etc.)
    reproductive_health = models.CharField(max_length=255, choices=GYN_STATUS_CHOICES, null=True, blank=True)  # Reproductive health choices
    reproductive_health_other = models.TextField(null=True, blank=True)  # Custom text if not in choices
    metabolic_disease = models.CharField(max_length=255, choices=METABOLIC_DISEASE_CHOICES, null=True, blank=True)  # Metabolic disease choices
    metabolic_disease_other = models.TextField(null=True, blank=True)  # Custom text if not in choices
    
    # Vaccination and Deworming
    vaccination_date = models.DateField(null=True, blank=True)  # Date and type of vaccination given
    deworming_date = models.DateField(null=True, blank=True)  # Date of deworming

    def __str__(self):
        return f"Animal {self.cow_id} - {self.breed} at {self.farm}"

