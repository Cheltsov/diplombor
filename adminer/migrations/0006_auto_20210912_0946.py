# Generated by Django 3.2.6 on 2021-09-12 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminer', '0005_auto_20210911_1310'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='category',
            table='category',
        ),
        migrations.CreateModel(
            name='CategoryPattern',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_category', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminer.category')),
                ('id_pattern', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminer.pattern')),
            ],
            options={
                'db_table': 'category_pattern',
                'managed': True,
            },
        ),
    ]
