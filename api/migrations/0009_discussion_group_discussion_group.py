# Generated by Django 5.1.1 on 2025-04-26 01:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_siteuser_token_generated_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='username', max_length=100)),
                ('discussion', models.TextField(max_length=2000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.reader')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('discussions', models.ManyToManyField(through='api.Discussion', to='api.reader')),
            ],
        ),
        migrations.AddField(
            model_name='discussion',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.group'),
        ),
    ]
