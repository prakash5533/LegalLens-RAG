from rest_framework import serializers
from .models import Document, ClauseAnalysis

class ClauseAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClauseAnalysis
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    clauses = ClauseAnalysisSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = '__all__'