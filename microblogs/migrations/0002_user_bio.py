# Generated by Django 4.1.1 on 2022-10-04 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microblogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
