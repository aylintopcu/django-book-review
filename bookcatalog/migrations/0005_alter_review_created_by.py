# Generated by Django 3.2.6 on 2021-08-10 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookcatalog', '0004_alter_review_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bookcatalog.reader'),
        ),
    ]