# Generated by Django 2.2.5 on 2021-04-19 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_auto_20210416_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to='room-photos'),
        ),
    ]