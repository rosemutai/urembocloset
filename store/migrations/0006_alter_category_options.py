# Generated by Django 5.2.1 on 2025-05-30 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_category_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
