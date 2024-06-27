# Generated by Django 5.0.6 on 2024-06-27 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_email_alter_user_is_active_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="oauth_platform",
            field=models.CharField(
                choices=[("", "None"), ("google", "Google"), ("naver", "Naver")], default="", max_length=50, null=True
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=255, null=True),
        ),
    ]