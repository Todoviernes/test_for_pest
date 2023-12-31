# Generated by Django 4.2.7 on 2023-11-10 18:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_appointment_statistics_testresult_testoperator_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Disease",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name="customer",
            name="phone",
            field=models.CharField(
                blank=True,
                default=0,
                max_length=17,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                        regex="^\\+?1?\\d{9,15}$",
                    )
                ],
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="testresult",
            name="disease",
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to="users.disease"),
            preserve_default=False,
        ),
    ]
