import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.contrib.postgres.fields import JSONField


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Survey(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128)
    description = models.TextField()
    is_collect_email_addresses = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.title} - {self.created_by} - {self.created_on}'


class SurveyQuestion(models.Model):

    QUESTION_TYPE_CHOICES = (
        ('SHORT', 'Short Answer'),
        ('PARAG', 'Paragraph'),
        ('MULTI', 'Multiple Choice'),
        ('CHECK', 'Checkboxes'),
        ('DROPD', 'Dropdown'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    order_no = models.PositiveIntegerField(default=0)
    question = models.CharField(max_length=256)
    question_type = models.CharField(
        max_length=10, choices=QUESTION_TYPE_CHOICES)
    is_required = models.BooleanField(default=True)
    configuration = JSONField(default=dict)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.survey.title} - {self.order_no} - {self.question}'


class SurveyResponse(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    email_address = models.CharField(max_length=64, null=True, blank=True)
    responded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.survey.title} => {self.responded_on} {self.email_address if self.email_address else ""}'


class SurveyResponseAnswer(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    survey_response = models.ForeignKey(
        SurveyResponse, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    survey_question = models.ForeignKey(
        SurveyQuestion, on_delete=models.CASCADE)
    answer = JSONField(default=dict)

    def __str__(self):
        return f'{self.id} => {self.survey_response}'

# docker-compose run web python manage.py makemigrations
# docker-compose run web python manage.py migrate
