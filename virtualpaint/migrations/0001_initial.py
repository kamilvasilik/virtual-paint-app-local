# Generated by Django 3.1.1 on 2020-10-13 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChosenColors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('huemin', models.IntegerField()),
                ('satmin', models.IntegerField()),
                ('valmin', models.IntegerField()),
                ('huemax', models.IntegerField()),
                ('satmax', models.IntegerField()),
                ('valmax', models.IntegerField()),
                ('B', models.IntegerField()),
                ('G', models.IntegerField()),
                ('R', models.IntegerField()),
            ],
        ),
    ]
