
import os
from transformers import pipeline

# Singleton pattern: We only want to load the heavy model ONCE
# not every time a user loads the page.
_summarizer_model = None

def load_model():
    global _summarizer_model
    
    if _summarizer_model is not None:
        return _summarizer_model

    print("Loading ML model into memory... (This happens only once)")
    
    local_path = "./my_summarizer_model"
    
    try:
        if os.path.exists(local_path):
            _summarizer_model = pipeline("summarization", model=local_path)
        else:
            print("Local model not found, downloading from Hugging Face...")
            _summarizer_model = pipeline("summarization", model="facebook/bart-large-cnn")
            
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

    return _summarizer_model

def get_summary(text, max_length=150, min_length=40, do_sample=False):
    """
    Enhanced function with customizable parameters
    """
    summarizer = load_model()
    if not summarizer:
        return "Error: Model could not be loaded."

    try:
        result = summarizer(
            text, 
            max_length=max_length, 
            min_length=min_length, 
            do_sample=do_sample
        )
        return result[0]['summary_text']
    except Exception as e:
        return f"Error during summarization: {str(e)}"