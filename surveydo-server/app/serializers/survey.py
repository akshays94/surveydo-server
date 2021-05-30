from rest_framework import serializers
from ..models import Survey


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


# class SurveyPatchSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Survey
#         fields = [
#             'title',
#             'description'
#         ]
    
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.save()
#         return instance
