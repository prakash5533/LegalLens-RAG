from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='legal_docs/')
    extracted_text = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    overall_risk_score = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ClauseAnalysis(models.Model):
    RISK_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='clauses')
    clause_title = models.CharField(max_length=255)
    original_text = models.TextField()
    simplified_text = models.TextField()
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES, default='Low')
    risk_explanation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document.title} - {self.clause_title} ({self.risk_level})"