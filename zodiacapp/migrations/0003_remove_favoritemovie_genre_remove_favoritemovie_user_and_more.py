# Generated by Django 4.2.13 on 2024-06-03 15:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("zodiacapp", "0002_comment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="favoritemovie",
            name="genre",
        ),
        migrations.RemoveField(
            model_name="favoritemovie",
            name="user",
        ),
        migrations.RemoveField(
            model_name="favoriteseries",
            name="genre",
        ),
        migrations.RemoveField(
            model_name="favoriteseries",
            name="user",
        ),
        migrations.RemoveField(
            model_name="relationshipstatus",
            name="friend",
        ),
        migrations.AddField(
            model_name="relationshipstatus",
            name="color",
            field=models.CharField(
                choices=[
                    ("red", "Red"),
                    ("green", "Green"),
                    ("blue", "Blue"),
                    ("yellow", "Yellow"),
                ],
                default="blue",
                help_text="Color for display",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="friendship",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("accepted", "Accepted"),
                    ("declined", "Declined"),
                ],
                default="pending",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="relationshipstatus",
            name="status",
            field=models.CharField(
                choices=[
                    ("Single", "Single"),
                    ("In a relationship", "In a relationship"),
                    ("Engaged", "Engaged"),
                    ("Married", "Married"),
                    ("Its complicated", "Its complicated"),
                ],
                default="Single",
                help_text="Relationship status",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="relationshipstatus",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="relationship_status",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(
            name="FavoriteBook",
        ),
        migrations.DeleteModel(
            name="FavoriteMovie",
        ),
        migrations.DeleteModel(
            name="FavoriteSeries",
        ),
        migrations.DeleteModel(
            name="Genre",
        ),
    ]
