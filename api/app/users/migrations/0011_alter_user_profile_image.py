# Generated by Django 5.0.6 on 2024-07-02 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_remove_naveruserid_user_remove_user_oauth_platform_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_image",
            field=models.CharField(
                default="https://live-streaming-list-profile.s3.amazonaws.com/profile_images/default_profile.png",
                max_length=255,
            ),
        ),
    ]