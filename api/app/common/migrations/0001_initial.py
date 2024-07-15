# Generated by Django 5.0.6 on 2024-06-19 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CommonModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("channel_name", models.CharField(max_length=255)),
                ("thumbnail", models.URLField(max_length=1024)),
                ("concurrent_viewers", models.PositiveIntegerField(default=0)),
                ("title", models.CharField(max_length=255)),
                (
                    "platform",
                    models.CharField(
                        choices=[("youtube", "YouTube"), ("chzzk", "Chzzk"), ("afreecatv", "AfreecaTV")],
                        default="youtube",
                        max_length=50,
                    ),
                ),
                ("streaming_link", models.URLField(max_length=1024)),
                ("channel_link", models.URLField(max_length=1024)),
                ("channel_description", models.TextField(null=True)),
                ("followers", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "라이브 스트리밍",
                "verbose_name_plural": "라이브 스트리밍 목록",
                "db_table": "live_streaming_table",
            },
        ),
    ]
