# Generated by Django 4.0.8 on 2022-12-03 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0008_delete_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
