from django.contrib import admin
from .models import Document, ClauseAnalysis

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'overall_risk_score', 'created_at')
    search_fields = ('title', 'summary')

@admin.register(ClauseAnalysis)
class ClauseAnalysisAdmin(admin.ModelAdmin):
    list_display = ('clause_title', 'document', 'risk_level', 'created_at')
    list_filter = ('risk_level',)
    search_fields = ('clause_title', 'original_text')