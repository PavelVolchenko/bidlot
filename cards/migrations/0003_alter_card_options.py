# Generated by Django 5.0.2 on 2024-02-18 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_alter_card_user_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['-created'], 'permissions': [('special_status', 'Can be used')]},
        ),
    ]
