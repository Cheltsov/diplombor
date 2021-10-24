from django.db import models
from django.db.models import Count
from django.utils import timezone


class Pattern(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    date_update = models.DateTimeField(auto_now=True, db_index=True, null=True)

    def get_category_id(self):
        return self.categorypattern_set.all().values_list('id_category_id', flat=True)

    class Meta:
        managed = True
        db_table = 'pattern'


class Polls(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, db_index=True, null=True)

    def get_category_id(self):
        return self.categorypolls_set.all().values_list('id_category_id', flat=True)

    def copy(self):
        questions = self.question_set.all()
        categories = self.categorypolls_set.all()
        obj = Polls(title=self.title, description=self.description, date_start=None, date_end=None)
        obj.save()
        for item_question in questions:
            answers = item_question.answer_set.all()
            obj_question = Question(
                title=item_question.title,
                id_pattern_id=item_question.id_pattern_id,
                id_category_id=item_question.id_category_id,
                id_polls_id=obj.id,
                is_verbal=item_question.is_verbal)
            obj_question.save()
            for item_answer in answers:
                obj_answer = Answer(title=item_answer.title, cost=item_answer.cost, id_question_id=obj_question.id)
                obj_answer.save()

        for item_category in categories:
            obj_categories = CategoryPolls(id_category_id=item_category.id_category_id, id_polls_id=obj.id)
            obj_categories.save()

    def getCountUserAnswer(self):
        return self.useranswer_set.values('user').annotate(count_user=Count('user')).count()

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
    sort = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'question'
        ordering = ['sort']


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE, default="", null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)
    sort = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'answer'
        ordering = ['sort']


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
    user = models.CharField(max_length=100, blank=True, null=True)
    is_category = models.BooleanField(blank=True, null=False, default=False)
    id_category_id = models.IntegerField(default=0)
    answer_cost = models.FloatField(max_length=20, null=True)

    class Meta:
        managed = True
        db_table = 'user_answer'

