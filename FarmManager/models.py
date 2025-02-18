from django.db import models

# Farm Model
class Farm(models.Model):
    farm_id = models.AutoField(primary_key=True)
    owner_name = models.CharField(max_length=255)
    address = models.TextField()
    telephone_number = models.CharField(max_length=15,
            validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',  # Allows international and local formats
            message="Enter a valid phone number (e.g. +251912345678 or 0912345678)."
        )],)
    location_gps = models.CharField(max_length=255, null=True, blank=True)
    fertility_camp_no = models.IntegerField()
    total_number_of_cows = models.IntegerField()
    number_of_calves = models.IntegerField()
    number_of_calf = models.IntegerField()
    number_of_milking_cow = models.IntegerField()
    total_daily_milk = models.IntegerField()
    type_of_housing = models.CharField(max_length=50, choices=[
        ('free stall', 'Free Stall'),
        ('tie stall', 'Tie Stall'),
        ('traditional', 'Traditional')
    ])
    type_of_floor = models.CharField(max_length=50, choices=[
        ('concrete', 'Concrete'),
        ('stone', 'Stone'),
        ('soil', 'Soil'),
        ('mat', 'Mat')
    ])
    main_feed = models.TextField()
    rate_of_cow_feeding = models.CharField(max_length=50, choices=[
        ('once', 'Once'),
        ('twice', 'Twice'),
        ('three times', 'Three Times')
    ])
    source_of_water = models.CharField(max_length=50, choices=[
        ('tap', 'Tap'),
        ('wells', 'Wells')
    ])
    rate_of_water_giving = models.CharField(max_length=50, choices=[
        ('once', 'Once'),
        ('twice', 'Twice'),
        ('three times', 'Three Times')
    ])
    farm_hygiene_score = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')])

# Cow Model
class Cow(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    cow_id = models.AutoField(primary_key=True)
    breed = models.CharField(max_length=100)
    age_in_days = models.IntegerField()
    sex = models.CharField(max_length=50, default='milking_cow')
    parity = models.IntegerField()
    body_weight = models.FloatField()
    bcs = models.FloatField(choices=[(1, '1'), (1.5, '1.5'), (2, '2'), (2.5, '2.5'), (3, '3'), (3.5, '3.5'), (4, '4'), (4.5, '4.5'), (5, '5')])
    gynecological_status = models.CharField(max_length=50, choices=[
        ('Estrus', 'Estrus'),
        ('AI', 'AI'),
        ('Pregna', 'Pregna')
    ])
    lactation_number = models.IntegerField()
    days_in_milk = models.IntegerField()
    average_daily_milk = models.FloatField()
    cow_inseminated_before = models.BooleanField()
    last_date_insemination = models.DateField()
    number_of_inseminations = models.IntegerField()
    id_or_breed_bull_used = models.IntegerField()
    last_calving_date = models.DateField()

# Health Model
class Health(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    udder_health = models.CharField(max_length=50, choices=[
        ('4qt', '4 Quarters'),
        ('3qt', '3 Quarters'),
        ('2qt', '2 Quarters'),
        ('1qt', '1 Quarter')
    ])
    mastitis = models.CharField(max_length=50, choices=[
        ('negative', 'Negative'),
        ('clinical mastitis', 'Clinical Mastitis')
    ])
    general_health = models.CharField(max_length=50, choices=[
        ('normal', 'Normal'),
        ('sick', 'Sick')
    ])
    reproductive_health = models.TextField()
    metabolic_health = models.TextField()
    is_cow_vaccinated = models.BooleanField()
    vaccination_date = models.DateField(null=True, blank=True)
    vaccination_type = models.TextField()
    has_cow_taken_deworming = models.BooleanField()
    deworming_date = models.DateField(null=True, blank=True)
    deworming_type = models.TextField()

# Reproduction Model
class Reproduction(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    is_cow_pregnant = models.BooleanField()
    heat_sign_start = models.DateTimeField()
    heat_sign_end = models.DateTimeField(null=True, blank=True)
    heat_signs_seen = models.TextField()
    pregnancy_date = models.DateField()
    calving_date = models.DateField()
