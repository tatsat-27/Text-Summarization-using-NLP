import nltk
import heapq
from flask import Flask


app = Flask(__name__)

def preprocess_text(text):
    # Tokenize the text into sentences and words
    sentence_list = nltk.sent_tokenize(text)
    word_list = nltk.word_tokenize(text)
    
    # Initializing stop words
    stopwords = nltk.corpus.stopwords.words('english')
    
    # Removing stopwords from the word list
    filtered_words = [word for word in word_list if word.lower() not in stopwords]
    
    return sentence_list, filtered_words

def calculate_word_frequencies(words):
    frequency_map = {}
    
    for word in words:
        if word not in frequency_map:
            frequency_map[word] = 1
        else:
            frequency_map[word] += 1
    
    max_frequency = max(frequency_map.values())
    
    for word in frequency_map:
        frequency_map[word] = frequency_map[word] / max_frequency
    
    return frequency_map

def calculate_sentence_scores(sentence_list, frequency_map):
    sent_score = {}
    
    for sent in sentence_list:
        for word in frequency_map:
            if word in frequency_map and len(sent.split(" ")) < 35:
                if sent not in sent_score:
                    sent_score[sent] = frequency_map[word]
                else:
                    sent_score[sent] += frequency_map[word]
    
    return sent_score

def generate_summary(sent_score, num_sentences=10):
    # Finding the top sentences based on scores
    summary = heapq.nlargest(num_sentences, sent_score, key=sent_score.get)
    
    return summary

def main():
    text = '''India is a country in South Asia, known for its rich history, diverse cultures, and vibrant traditions. It is the seventh-largest country by land area and the second-most populous country in the world. India is characterized by a variety of landscapes, including the Himalayan mountain range in the north and the vast Gangetic plains.

The capital of India is New Delhi, and the largest city is Mumbai. The country has a parliamentary system of government and is a federal republic. India gained independence from British rule on August 15, 1947.

India is culturally diverse, with a multitude of languages, religions, and ethnic groups. Hindi and English are the official languages, and there are 22 officially recognized regional languages. Hinduism, Islam, Christianity, Sikhism, Buddhism, and Jainism are some of the major religions practiced in the country.

The Indian economy is one of the world's largest, with a mix of traditional village farming and modern industries. Information technology, pharmaceuticals, and telecommunications are some of the rapidly growing sectors.

India has a rich cultural heritage, including classical art forms, music, dance, and architecture. Popular landmarks include the Taj Mahal, Jaipur's palaces, and ancient temples like Khajuraho and Konark. The country also has a thriving film industry, commonly known as Bollywood.

Tourists are drawn to India for its diverse landscapes, historical sites, and festivals. Notable festivals include Diwali, Holi, Eid, and various regional celebrations.'''
    
    # Check if the input text is empty or contains only spaces
    if text.isspace() or not text:
        print("Text is empty. Nothing to summarize.")
        return
    
    sentence_list, filtered_words = preprocess_text(text)
    frequency_map = calculate_word_frequencies(filtered_words)
    sent_score = calculate_sentence_scores(sentence_list, frequency_map)
    summary = generate_summary(sent_score, num_sentences=10)
    
    for sentence in summary:
        print(sentence)

if __name__ == "__main__":
    main()
