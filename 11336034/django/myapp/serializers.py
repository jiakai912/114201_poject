from rest_framework import serializers
from .models import Dream, Comment, DreamAnalysis

class DreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dream
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class DreamAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = DreamAnalysis
        fields = '__all__'
