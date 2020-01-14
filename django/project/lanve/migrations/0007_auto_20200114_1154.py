# Generated by Django 3.0.1 on 2020-01-14 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lanve', '0006_lanveuser_count_view'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lanveuser',
            name='count_view',
        ),
        migrations.AddField(
            model_name='issue',
            name='count_view',
            field=models.PositiveIntegerField(default=0, verbose_name='the number of this issue view'),
        ),
    ]