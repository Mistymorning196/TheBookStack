# Generated by Django 5.1.1 on 2025-04-03 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookgenre',
            name='name',
            field=models.CharField(default='name', max_length=100),
        ),
        migrations.AlterField(
            model_name='readergenre',
            name='name',
            field=models.CharField(default='name', max_length=100),
        ),
    ]
