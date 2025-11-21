from rest_framework import serializers
from django.core.validators import MinLengthValidator

class SummarizeSerializer(serializers.Serializer):
    text = serializers.CharField(
        validators=[MinLengthValidator(50)],
        help_text="Text to summarize (minimum 50 characters)"
    )
    max_length = serializers.IntegerField(
        required=False, 
        default=150,
        min_value=50,
        max_value=500,
        help_text="Maximum length of summary (default: 150)"
    )
    min_length = serializers.IntegerField(
        required=False, 
        default=40,
        min_value=20,
        max_value=200,
        help_text="Minimum length of summary (default: 40)"
    )

class SummaryResponseSerializer(serializers.Serializer):
    original_text = serializers.CharField(read_only=True)
    summary = serializers.CharField(read_only=True)
    original_length = serializers.IntegerField(read_only=True)
    summary_length = serializers.IntegerField(read_only=True)
    reduction_ratio = serializers.FloatField(read_only=True)
    processing_time = serializers.FloatField(read_only=True)