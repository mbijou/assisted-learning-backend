# Generated by Django 3.1.4 on 2021-01-04 22:08

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('multiple_choices', '0002_multiplechoiceanswer'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MultipleChoiceAnswer',
            new_name='MultipleChoiceSolutionAnswer',
        ),
    ]
