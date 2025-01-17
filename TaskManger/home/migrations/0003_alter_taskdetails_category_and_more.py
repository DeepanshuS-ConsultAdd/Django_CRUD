# Generated by Django 5.0.7 on 2024-07-24 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_taskdetails_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskdetails',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='taskdetails',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='taskdetails',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='taskdetails',
            name='priority',
            field=models.IntegerField(blank=True, default=5, null=True),
        ),
    ]
