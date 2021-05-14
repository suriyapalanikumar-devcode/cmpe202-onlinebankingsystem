# Generated by Django 3.1.7 on 2021-05-12 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payees', '0002_auto_20210506_1656'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='payee',
            constraint=models.UniqueConstraint(fields=('payeeName', 'user'), name='uk_payee_name'),
        ),
    ]
