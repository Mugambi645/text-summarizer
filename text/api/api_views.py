import time
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..services.ml_services import get_summary
from .serializers import SummarizeSerializer, SummaryResponseSerializer

@api_view(['POST'])
def summarize_api(request):
    """
    API endpoint for text summarization
    """
    serializer = SummarizeSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {
                'error': 'Validation failed',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    validated_data = serializer.validated_data
    text = validated_data['text']
    max_length = validated_data.get('max_length', 150)
    min_length = validated_data.get('min_length', 40)
    
    # Start timing
    start_time = time.time()
    
    try:
        # Get summary with custom parameters
        summary = get_summary(text, max_length=max_length, min_length=min_length)
        
        # Calculate metrics
        processing_time = round(time.time() - start_time, 2)
        original_length = len(text.split())
        summary_length = len(summary.split())
        reduction_ratio = round(((original_length - summary_length) / original_length) * 100, 1)
        
        response_data = {
            'original_text': text,
            'summary': summary,
            'original_length': original_length,
            'summary_length': summary_length,
            'reduction_ratio': reduction_ratio,
            'processing_time': processing_time
        }
        
        response_serializer = SummaryResponseSerializer(response_data)
        return Response(response_serializer.data)
        
    except Exception as e:
        return Response(
            {
                'error': 'Summarization failed',
                'details': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def api_status(request):
    """
    API health check endpoint
    """
    from ..services.ml_services import load_model
    
    try:
        model = load_model()
        status_info = {
            'status': 'healthy',
            'model_loaded': model is not None,
            'message': 'Text summarization API is running correctly'
        }
    except Exception as e:
        status_info = {
            'status': 'error',
            'model_loaded': False,
            'message': f'API error: {str(e)}'
        }
    
    return Response(status_info)