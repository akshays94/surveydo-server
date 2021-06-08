from rest_framework import serializers
from ..models import Survey
from ..models import SurveyQuestion
from ..models import SurveyResponse
from ..models import SurveyResponseAnswer


class SurveySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Survey
        fields = [
            'id',
            'title',
            'description',
            'modified_on',
            'is_collect_email_addresses'
        ]


class SurveyResponseSerializer(serializers.Serializer):

    email_address = serializers.EmailField(required=True)
    answers = serializers.JSONField(required=True)

    def validate(self, data):
        survey = self.context['survey']
        answers = data['answers']

        email_address = None
        if survey.is_collect_email_addresses:
            email_address = data.get('email_address')
            if email_address:
                is_already_submitted = survey.surveyresponse_set.filter(email_address=email_address).exists()
                if is_already_submitted:
                    raise serializers.ValidationError({
                        'message': f'Already recorded response for email address: {email_address}'
                    })
        else:
            data['email_address'] = None

        survey_questions = survey.surveyquestion_set.all().values('id', 'is_required')

        required_question_ids = set(map(lambda i: str(i['id']), filter(lambda q: q['is_required'], survey_questions)))

        answered_question_ids = set(answers.keys())

        all_question_ids = set(map(lambda q: str(q['id']), survey_questions))
        
        unwanted_question_ids = all_question_ids - answered_question_ids
        if unwanted_question_ids:
            raise serializers.ValidationError({
                'message': 'Unwanted question(s) found'
            })

        unanswered_question_ids = required_question_ids - answered_question_ids
        if unanswered_question_ids:
            raise serializers.ValidationError({
                'message': 'Required questions unanswered'
            })

        for question_id, answer_item in answers.items():

            for key in answer_item.keys():
                if key not in ['title', 'other']:
                    del answer_item['key']

            question = SurveyQuestion.objects.get(id=question_id)
            title = answer_item['title']
            other = answer_item['other']
            
            if question.question_type in ['SHORT', 'PARAG', 'DROPD']:
                answer_item.update({'other': None})
            
            if question.question_type in ['MULTI', 'CHECK', 'DROPD']:
                options = set(map(lambda o: o['title'], question.configuration['options']))
                if title not in options:
                    raise serializers.ValidationError({
                        'message': 'Invalid option selected'
                    })

                if question.question_type in ['MULTI', 'CHECK']:
                    is_add_other = question.configuration.get('isAddOther', False)
                    if not is_add_other:
                        answer_item.update({'other': None})    

        data.update({
            'survey': survey
        })
        return data

    def create(self, validated_data):
        survey = validated_data['survey']
        email_address = validated_data['email_address']
        answers = validated_data['answers']

        survey_response = SurveyResponse.objects.create(**{
            'survey': survey,
            'email_address': email_address
        })

        response_objects = list()
        for question_id, answer_item in answers.items():
            response_objects.append(
                SurveyResponseAnswer(**{
                    'survey_response': survey_response,
                    'survey': survey,
                    'survey_question': SurveyQuestion.objects.get(id=question_id),
                    'answer': answer_item,
                })
            )
        SurveyResponseAnswer.objects.bulk_create(response_objects)

        # print(survey_response.__dict__)

        # for x in survey_response.surveyresponseanswer_set.all():
        #     print(x.__dict__)

        return survey_response
