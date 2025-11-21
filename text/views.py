from django.shortcuts import render, redirect
from django.http import JsonResponse
from .services.ml_services import get_summary

def home(request):
    """Home page with input form"""
    return render(request, 'home.html')

def summarize_text(request):
    """Handle form submission and generate summary"""
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        
        if not text:
            return render(request, 'my_app/home.html', {
                'error': 'Please enter some text to summarize.',
                'text': text
            })
        
        if len(text) < 50:
            return render(request, 'my_app/home.html', {
                'error': 'Text is too short. Please enter at least 50 characters.',
                'text': text
            })
        
        # Generate summary
        summary = get_summary(text)
        
        # Calculate reduction ratio
        original_words = len(text.split())
        summary_words = len(summary.split())
        reduction_ratio = int(((original_words - summary_words) / original_words) * 100) if original_words > 0 else 0
        
        return render(request, 'results.html', {
            'original_text': text,
            'summary': summary,
            'reduction_ratio': reduction_ratio
        })
    
    return redirect('home')

def api_summarize(request):
    """API endpoint for AJAX requests"""
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        
        if not text or len(text) < 50:
            return JsonResponse({'error': 'Text must be at least 50 characters'}, status=400)
        
        summary = get_summary(text)
        return JsonResponse({'summary': summary})
    
    return JsonResponse({'error': 'Only POST requests allowed'}, status=405)