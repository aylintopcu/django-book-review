# Generated by Django 3.2.6 on 2021-09-02 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookcatalog', '0012_reader_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reader',
            name='profile_picture',
        ),
    ]