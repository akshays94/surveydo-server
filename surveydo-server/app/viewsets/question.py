from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import SurveyQuestion
from ..serializers.question import SurveyQuestionSerializer


class SurveyQuestionViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):

    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer

    def destroy(self, request, pk=None):
        question = get_object_or_404(SurveyQuestion, pk=pk)
        survey_id = question.survey_id
        question.delete()
        questions = SurveyQuestion.objects.filter(
            survey_id=survey_id).order_by('order_no')
        for i, question in enumerate(questions):
            question.order_no = i + 1
            question.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
