# Generated by Django 3.2.6 on 2021-09-22 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminer', '0015_rename_id_category_useranswer_id_category_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='id_category_id',
            field=models.IntegerField(default=0),
        ),
    ]