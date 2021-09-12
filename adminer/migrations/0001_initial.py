# Generated by Django 3.2.6 on 2021-08-28 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pattern',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_update', models.DateTimeField(auto_now=True, db_index=True)),
            ],
            options={
                'db_table': 'pattern',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Polls',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_start', models.DateTimeField(blank=True, null=True)),
                ('date_end', models.DateTimeField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(auto_now=True, db_index=True)),
            ],
            options={
                'db_table': 'polls',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('id_pattern', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='adminer.pattern')),
                ('id_polls', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='adminer.polls')),
            ],
            options={
                'db_table': 'question',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PollsPattern',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_pattern', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='adminer.pattern')),
                ('id_polls', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='adminer.polls')),
            ],
            options={
                'db_table': 'polls_pattern',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.IntegerField(blank=True, null=True)),
                ('cost', models.IntegerField(blank=True, null=True)),
                ('id_question', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='adminer.question')),
            ],
            options={
                'db_table': 'answer',
                'managed': True,
            },
        ),
    ]