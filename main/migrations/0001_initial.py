# Generated by Django 2.2.13 on 2023-02-22 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activityId', models.CharField(default=None, max_length=30)),
                ('attraction_type', models.CharField(choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High'), ('4', 'Thrilling')], max_length=20)),
                ('price', models.PositiveIntegerField(default=None)),
            ],
            options={
                'verbose_name_plural': 'Activity',
                'ordering': ['activityId'],
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookingID', models.CharField(default=None, max_length=30)),
                ('start_date', models.DateTimeField(default=None, null=True)),
                ('end_date', models.DateTimeField(default=None, null=True)),
                ('status', models.BooleanField(default=False)),
                ('waiting', models.BooleanField(default=False)),
                ('attraction_type', models.CharField(choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High'), ('4', 'Thrilling')], max_length=20)),
                ('booktime', models.DateField()),
                ('activity_allocated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.activity')),
                ('user_booked', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-booktime'],
            },
        ),
        migrations.CreateModel(
            name='WaitingOn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_booked', models.DateField(default=django.utils.timezone.now)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('resID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Reservation')),
            ],
            options={
                'verbose_name_plural': 'WaitingOn',
            },
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('reservation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Reservation')),
            ],
            options={
                'verbose_name_plural': 'Visitors',
            },
        ),
        migrations.CreateModel(
            name='PreReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('attraction_type', models.CharField(choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High'), ('4', 'Thrilling')], max_length=20)),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.activity')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedbackID', models.CharField(default=None, max_length=100)),
                ('time', models.DateField(default=django.utils.timezone.now)),
                ('feed', models.TextField(default=None)),
                ('user_of', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-time'],
            },
        ),
    ]
