# Generated by Django 4.2.7 on 2023-11-24 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billy', '0011_alter_pointtransaction_points_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pointtransaction',
            name='sender',
        ),
    ]