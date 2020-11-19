# Generated by Django 3.1.3 on 2020-11-19 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars_rest_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='rating',
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars_rest_api.car')),
            ],
        ),
    ]
