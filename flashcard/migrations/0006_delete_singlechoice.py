# Generated by Django 3.1.4 on 2020-12-23 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0005_solution_answer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SingleChoice',
        ),
    ]
