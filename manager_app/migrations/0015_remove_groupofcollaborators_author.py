# Generated by Django 4.0.8 on 2022-12-03 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0014_remove_groupofcollaborators_collaborators'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupofcollaborators',
            name='author',
        ),
    ]
