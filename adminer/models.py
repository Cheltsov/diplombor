from django.db import models
from django.utils import timezone


class Pattern(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    date_update = models.DateTimeField(auto_now=True, db_index=True, null=True)

    def get_category_id(self):
        return self.categorypattern_set.all().values_list('id_category_id', flat=True)

    class Meta:
        managed = True
        db_table = 'pattern'


class Polls(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, db_index=True, null=True)

    def get_category_id(self):
        return self.categorypolls_set.all().values_list('id_category_id', flat=True)

    class Meta:
        managed = True
        db_table = 'polls'


class PollsPattern(models.Model):
    id = models.AutoField(primary_key=True)
    id_polls = models.ForeignKey(Polls, on_delete=models.CASCADE, default="")
    id_pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, default="")

    class Meta:
        managed = True
        db_table = 'polls_pattern'


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, db_index=True, null=True)

    class Meta:
        managed = True
        db_table = 'category'


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    id_polls = models.ForeignKey(Polls, on_delete=models.SET_NULL, default="", null=True)
    id_pattern = models.ForeignKey(Pattern, on_delete=models.SET_NULL, default="", null=True)
    is_verbal = models.BooleanField(blank=True, null=False, default=False)
    id_category = models.ForeignKey(Category, on_delete=models.SET_NULL, default="", null=True)

    class Meta:
        managed = True
        db_table = 'question'


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE, default="", null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'answer'


class CategoryPattern(models.Model):
    id = models.AutoField(primary_key=True)
    id_category = models.ForeignKey(Category, on_delete=models.SET_NULL, default="", null=True)
    id_pattern = models.ForeignKey(Pattern, on_delete=models.SET_NULL, default="", null=True)

    class Meta:
        managed = True
        db_table = 'category_pattern'


class CategoryPolls(models.Model):
    id = models.AutoField(primary_key=True)
    id_category = models.ForeignKey(Category, on_delete=models.SET_NULL, default="", null=True)
    id_polls = models.ForeignKey(Polls, on_delete=models.SET_NULL, default="", null=True)

    class Meta:
        managed = True
        db_table = 'category_polls'


class UserAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    id_polls = models.ForeignKey(Polls, on_delete=models.SET_NULL, default="", null=True)
    id_question = models.ForeignKey(Question, on_delete=models.SET_NULL, default="", null=True)
    id_answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, default="", null=True)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, db_index=True, null=True)
    ip = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_answer'

