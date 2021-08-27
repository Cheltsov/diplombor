from django.db import models


class Answer(models.Model):
    id = models.AutoField(unique=True)
    id_question = models.IntegerField(blank=True, null=True)
    title = models.IntegerField(blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'answer'


class Pattern(models.Model):
    id = models.AutoField(unique=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pattern'


class Polls(models.Model):
    id = models.AutoField(unique=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    date_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'polls'


class PollsPattern(models.Model):
    id = models.AutoField(unique=True)
    id_polls = models.IntegerField(blank=True, null=True)
    id_pattern = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'polls_pattern'


class Question(models.Model):
    id = models.AutoField(unique=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    id_polls = models.IntegerField(blank=True, null=True)
    id_patter = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'question'
