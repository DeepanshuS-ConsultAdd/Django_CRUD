# Generated by Django 5.0.7 on 2024-07-24 02:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskdetails',
            name='category',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='taskdetails',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='taskdetails',
            name='due_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='taskdetails',
            name='priority',
            field=models.IntegerField(default=5),
        ),
    ]