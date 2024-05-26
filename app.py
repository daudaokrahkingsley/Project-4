from flask import Flask, request, render_template
import spacy
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Initialize the spaCy model
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

def generate_wordcloud(text):
    doc = nlp(text)
    words = [token.text for token in doc if token.is_alpha]
    word_freq = Counter(words)
    
    # Generate WordCloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
    
    # Save the wordcloud image
    wordcloud.to_file("static/wordcloud.png")
    
    return word_freq, "static/wordcloud.png"

@app.route('/', methods=['GET', 'POST'])
def index():
    word_freq = {}
    wordcloud_image = None
    
    if request.method == 'POST':
        file = request.files['file']
        if file:
            text = file.read().decode('utf-8')
            word_freq, wordcloud_image = generate_wordcloud(text)
    
    return render_template('index.html', word_freq=word_freq, wordcloud_image=wordcloud_image)

if __name__ == '__main__':
    app.run(debug=True)
