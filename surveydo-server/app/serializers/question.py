from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import SurveyQuestion


class SurveyQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SurveyQuestion
        fields = [
            'id',
            'order_no',
            'survey',
            'question',
            'question_type',
            'is_required',
            'configuration'
        ]
        read_only_fields = ['order_no']
        validators = [
            UniqueTogetherValidator(
                queryset=SurveyQuestion.objects.all(),
                fields=['survey', 'question'],
                message='This question already exists'
            )
        ]

    def validate(self, data):
        is_create_case = self.instance is None

        if is_create_case:
            last_question = \
                SurveyQuestion.objects.filter(
                    survey=data['survey']).order_by('id').last()
            data['order_no'] = \
                last_question.order_no + 1 if last_question else 1

        return data

    def create(self, validated_data):
        survey = validated_data['survey']
        question = SurveyQuestion.objects.create(**validated_data)

        survey.modified_on = datetime.now()
        survey.save()

        return question

    def update(self, instance, validated_data):
        survey = validated_data['survey']
        instance.question = validated_data.get(
            'question', instance.question)
        instance.question_type = validated_data.get(
            'question_type', instance.question_type)
        instance.is_required = validated_data.get(
            'is_required', instance.is_required)
        instance.configuration = validated_data.get(
            'configuration', instance.configuration)
        instance.save()

        survey.modified_on = datetime.now()
        survey.save()

        return instance
