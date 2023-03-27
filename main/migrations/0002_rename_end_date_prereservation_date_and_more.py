# Generated by Django 4.1.7 on 2023-03-27 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prereservation',
            old_name='end_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='end_date',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='prereservation',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='waiting',
        ),
        migrations.AddField(
            model_name='prereservation',
            name='seats',
            field=models.PositiveIntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='activity',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='prereservation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.DeleteModel(
            name='WaitingOn',
        ),
    ]
