# Generated by Django 4.2.5 on 2023-10-06 08:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('price', models.FloatField()),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='media/hotels')),
                ('top_deal', models.BooleanField(default=False)),
                ('location', models.CharField(default='YourDefaultLocation', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('rating', models.PositiveIntegerField(choices=[(1, '1 Star'), (2, '2 Star'), (3, '3 Star'), (4, '4 Star'), (5, '5 Star')])),
                ('rating_date', models.DateTimeField(auto_now_add=True)),
                ('hotels', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='hotels.hotel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('hotels', 'user')},
            },
        ),
    ]
