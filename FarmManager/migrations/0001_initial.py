# Generated by Django 5.1 on 2024-12-29 12:23

import django.db.models.deletion
import multiselectfield.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farm_id', models.CharField(blank=True, max_length=50, unique=True)),
                ('owner_name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('telephone', models.CharField(max_length=15)),
                ('gps_location', models.CharField(blank=True, max_length=255, null=True)),
                ('fcc_no', models.CharField(blank=True, max_length=50, null=True)),
                ('herd_size', models.IntegerField()),
                ('calves', models.IntegerField()),
                ('heifers', models.IntegerField()),
                ('milking_cows', models.IntegerField()),
                ('tdm', models.FloatField(help_text='Total Daily Milk produced by the farm in liters')),
                ('housing_type', models.CharField(choices=[('free_stall', 'Free Stall'), ('tie_stall', 'Tie Stall'), ('traditional', 'Traditional')], max_length=20)),
                ('floor_type', models.CharField(choices=[('concrete', 'Concrete'), ('stone', 'Stone'), ('soil', 'Soil'), ('mat_bedding', 'Mat or Other Bedding')], max_length=20)),
                ('feed_given', models.TextField(help_text='Main feed given to the cows')),
                ('feeding_frequency', models.CharField(help_text='e.g. Once/day, twice/day, three times/day', max_length=50)),
                ('watering_frequency', models.CharField(help_text='e.g. Once/day, twice/day, three times/day', max_length=50)),
                ('farm_hygiene_score', models.IntegerField(help_text='Farm hygiene score from 1 to 4')),
            ],
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cow_id', models.CharField(max_length=50, unique=True)),
                ('breed', models.CharField(choices=[('hf', 'HF'), ('zebu', 'Zebu'), ('hf_zebu', 'HF*Zebu Cross'), ('other', 'Other')], max_length=50)),
                ('age_months', models.IntegerField()),
                ('sex', models.CharField(choices=[('milking', 'Milking Cow'), ('bull', 'Bull')], max_length=20)),
                ('parity', models.IntegerField()),
                ('body_weight', models.FloatField()),
                ('bcs', models.FloatField(choices=[(1.0, '1.0'), (1.5, '1.5'), (2.0, '2.0'), (2.5, '2.5'), (3.0, '3.0'), (3.5, '3.5'), (4.0, '4.0'), (4.5, '4.5'), (5.0, '5.0')])),
                ('gyn_status', models.CharField(choices=[('estrus', 'Estrus'), ('ai', 'AI'), ('pregnant', 'Pregnant'), ('abortion', 'Abortion'), ('fresh', 'Fresh')], max_length=20)),
                ('pd_status', models.CharField(choices=[('pregnant', 'Pregnant'), ('non_pregnant', 'Non-pregnant'), ('unknown', 'Unknown')], max_length=20)),
                ('days_to_calving', models.IntegerField(blank=True, null=True)),
                ('date_of_calving', models.DateField(blank=True, null=True)),
                ('lactation_no', models.IntegerField()),
                ('no_days_in_milk', models.IntegerField(default=0)),
                ('average_daily_milk', models.FloatField()),
                ('days_after_calving', models.IntegerField()),
                ('insemination_number', models.IntegerField()),
                ('date_ai', models.DateField(blank=True, null=True)),
                ('last_heat_sign', models.DateField(blank=True, null=True)),
                ('heat_signs', multiselectfield.db.fields.MultiSelectField(choices=[('bellowing', 'Bellowing'), ('restlessness', 'Restlessness'), ('off_feed', 'Off Feed'), ('vaginal_discharge', 'Vaginal Discharge'), ('mounting_other_cows', 'Mounting Other Cows'), ('standing_to_be_mounted', 'Standing to be Mounted'), ('head_butting_others', 'Head Butting Others'), ('chin_resting', 'Chin Resting')], max_length=200)),
                ('conception_rate', models.CharField(blank=True, choices=[('low', 'Low'), ('moderate', 'Moderate'), ('high', 'High')], max_length=20, null=True)),
                ('udder_health', models.CharField(choices=[('4qt_normal', '4qt normal'), ('3qt_normal', '3qt normal'), ('2qt_normal', '2qt normal'), ('1qt_normal', '1qt normal')], max_length=255)),
                ('mastitis', models.CharField(choices=[('negative', 'Negative'), ('clinical_mastitis', 'Clinical Mastitis'), ('cmt_positive', 'CMT +'), ('cmt_double_positive', 'CMT ++'), ('cmt_triple_positive', 'CMT +++')], max_length=255)),
                ('general_health', models.CharField(max_length=255)),
                ('reproductive_health', models.CharField(blank=True, choices=[('estrus', 'Estrus'), ('ai', 'AI'), ('pregnant', 'Pregnant'), ('abortion', 'Abortion'), ('fresh', 'Fresh')], max_length=255, null=True)),
                ('reproductive_health_other', models.TextField(blank=True, null=True)),
                ('metabolic_disease', models.CharField(blank=True, choices=[('hypocalcemia', 'Hypocalcemia'), ('vit_a_deficiency', 'Vitamin A Deficiency'), ('mg_deficiency', 'Magnesium Deficiency'), ('ketosis', 'Ketosis'), ('acidosis', 'Acidosis')], max_length=255, null=True)),
                ('metabolic_disease_other', models.TextField(blank=True, null=True)),
                ('vaccination_date', models.DateField(blank=True, null=True)),
                ('deworming_date', models.DateField(blank=True, null=True)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FarmManager.farm')),
            ],
        ),
    ]