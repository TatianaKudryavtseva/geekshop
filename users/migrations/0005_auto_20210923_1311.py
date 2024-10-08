# Generated by Django 3.2.6 on 2021-09-23 10:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_activation_key_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 25, 10, 11, 47, 349071, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagline', models.CharField(blank=True, max_length=128, verbose_name='????')),
                ('aboutMe', models.TextField(blank=True, max_length=512, verbose_name='? ????')),
                ('gender', models.CharField(blank=True, choices=[('M', 'М'), ('W', 'Ж')], max_length=1, verbose_name='???')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
