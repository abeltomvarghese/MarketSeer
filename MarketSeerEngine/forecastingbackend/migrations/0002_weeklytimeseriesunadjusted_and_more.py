# Generated by Django 4.0.5 on 2022-08-17 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecastingbackend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyTimeseriesUnadjusted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekly_symbol', models.CharField(max_length=10)),
                ('stock_open', models.DecimalField(decimal_places=4, max_digits=10)),
                ('stock_high', models.DecimalField(decimal_places=4, max_digits=10)),
                ('stock_low', models.DecimalField(decimal_places=4, max_digits=10)),
                ('stock_close', models.DecimalField(decimal_places=4, max_digits=10)),
                ('stock_adj_close', models.DecimalField(decimal_places=4, max_digits=10)),
                ('stock_volume', models.BigIntegerField()),
                ('dividend_amount', models.DecimalField(decimal_places=4, max_digits=10)),
                ('cobdate_partition', models.DateField()),
            ],
            options={
                'db_table': 'weekly_timeseries_unadjusted',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='DailyTimeseriesUnadjusted',
        ),
    ]