# sentiment_analysis.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

# Load pre-trained GPT-based model and tokenizer for sentiment analysis
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

sentiment_pipeline = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_words = [w for w in words if w.lower() not in stop_words]
    return ' '.join(filtered_words)

def get_sentiment(text):
    return sentiment_pipeline(text)[0]

if __name__ == "__main__":
    sample_text = "Apple stock is expected to rise due to strong earnings."
    preprocessed_text = preprocess_text(sample_text)
    print(get_sentiment(preprocessed_text))
