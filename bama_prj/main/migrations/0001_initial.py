# Generated by Django 2.1.7 on 2019-04-09 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarInfo',
            fields=[
                ('car_id', models.AutoField(primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=200)),
                ('model', models.CharField(max_length=200)),
                ('series', models.CharField(max_length=2000)),
                ('releaseDate', models.CharField(max_length=2000)),
                ('odo_meter', models.IntegerField()),
                ('cash_price', models.IntegerField()),
                ('pre_pay', models.IntegerField()),
                ('each_ins_amount', models.IntegerField()),
                ('ins_num', models.IntegerField()),
                ('description', models.CharField(max_length=500)),
            ],
        ),
    ]
