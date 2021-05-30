from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Survey
from ..serializers.survey import SurveySerializer
from ..serializers.question import SurveyQuestionSerializer


class SurveyViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):

    serializer_class = SurveySerializer
    pagination_class = None

    def get_queryset(self):
        return Survey.objects.filter(
            created_by=self.request.user).order_by('-created_on')

    def retrieve(self, request, pk=None):
        survey = get_object_or_404(Survey, pk=pk)
        questions = survey.surveyquestion_set.all().order_by('order_no')
        # for i, q in enumerate(questions):
        #     q.order_no = i + 1
        #     q.save()
        survey = SurveySerializer(survey).data
        survey.update({
            'questions': SurveyQuestionSerializer(questions, many=True).data
        })
        return Response(survey)

    @action(url_path='partial', methods=['patch'], detail=True)
    def perform_partial_update(self, request, pk=None):
        survey = get_object_or_404(Survey, pk=pk)
        survey.title = request.data.get('title', survey.title)
        survey.description = request.data.get('description', survey.description)
        survey.save()
        return Response()

    @action(url_path='untitled-survey', methods=['post'], detail=False)
    def create_untitled_survey(self, request):
        survey = Survey.objects.create(**{
            'title': 'Untitled Survey',
            'created_by': request.user
        })
        return Response(SurveySerializer(survey).data)

    @action(url_path='questions', methods=['get'], detail=True)
    def get_questions(self, request, pk=None):
        survey = get_object_or_404(Survey, pk=pk)
        questions = survey.surveyquestion_set.all().order_by('order_no')
        return Response(
            SurveyQuestionSerializer(questions, many=True).data
        )
