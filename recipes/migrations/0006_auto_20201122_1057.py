# Generated by Django 3.1.3 on 2020-11-22 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20201122_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='difficulty',
            field=models.CharField(choices=[('1', 'Easy'), ('2', 'Fair'), ('3', 'Moderate'), ('4', 'Difficult'), ('5', 'Expert')], default=3, max_length=1),
        ),
    ]
