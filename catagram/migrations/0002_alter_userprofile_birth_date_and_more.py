# Generated by Django 4.1.7 on 2023-04-15 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catagram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]