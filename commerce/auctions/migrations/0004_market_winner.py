# Generated by Django 4.0.3 on 2022-07-23 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_wl_no_alter_wl_user_alter_wl_wl'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='winner',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]