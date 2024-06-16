import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
import nltk
nltk.download('stopwords')
import nltk
nltk.download('wordnet')
import nltk
nltk.download('vader_lexicon')

class Emotions:

    def __init__(self, text):
        # text = open('read.txt', encoding='utf-8').read()
        lower_case = text.lower()
        self.cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

        # Using word_tokenize because it's faster than split()
        tokenized_words = word_tokenize(self.cleaned_text, "english")

        # Removing Stop Words
        final_words = []
        for word in tokenized_words:
            if word not in stopwords.words('english'):
                final_words.append(word)

        # Lemmatization - From plural to single + Base form of a word (example better-> good)
        lemma_words = []
        for word in final_words:
            word = WordNetLemmatizer().lemmatize(word)
            lemma_words.append(word)

        emotion_list = []
        with open('C:/Users/prady/Desktop/Project/Dependencies/emotions.txt', 'r') as file:
            for line in file:
                clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
                word, emotion = clear_line.split(':')

                if word in lemma_words:
                    emotion_list.append(emotion)

        # print(emotion_list)
        self.w = Counter(emotion_list)
        # print(w)

    def analyze_sentiment(self):
            score = SentimentIntensityAnalyzer().polarity_scores(self.cleaned_text)

            print(score)
            
            if score['neg'] > score['pos']:
                return "Negative Sentiment"
            elif score['neg'] < score['pos']:
                return "Positive Sentiment"
            else:
                return "Neutral Sentiment"

    def sentiment_graph(self):
        fig, ax1 = plt.subplots()
        plt.xlabel("Emotions")
        plt.ylabel("Count")
        ax1.bar(self.w.keys(), self.w.values())
        fig.autofmt_xdate()
        plt.savefig('C:/Users/prady/Desktop/Project/Dependencies/graph.png')

    def show_sentiment_graph(self):
        plt.show()


if __name__ == "__main__":
    nlp = Emotions(open('C:/Users/prady/Desktop/Project/Dependencies/read.txt', encoding='utf-8').read())
    print(nlp.analyze_sentiment())
    nlp.sentiment_graph()
    nlp.show_sentiment_graph()
