# Generated by Django 3.0.6 on 2021-01-25 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Diary', '0014_moodnote'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventnote',
            name='isaddphoto',
            field=models.CharField(default=True, max_length=50),
            preserve_default=False,
        ),
    ]