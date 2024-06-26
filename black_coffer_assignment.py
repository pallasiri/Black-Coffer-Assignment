# -*- coding: utf-8 -*-
"""Black Coffer Assignment

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KVbU4wsayzS5fnmb2qXX1spVSgRPwIBj

# Importing Packages
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ureq
import requests
import urllib
import re
import os

data = pd.read_excel("Input.xlsx")

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

data['URL']

article_titles = []
for i, url in enumerate(data['URL']):
    response_code = requests.get(url)
    soup = bs(response_code.text, 'html.parser')
    article_title = soup.find('title').text
    article_titles.append(article_title)

article_titles

url = 'https://insights.blackcoffer.com/rising-it-cities-and-its-impact-on-the-economy-environment-infrastructure-and-city-life-by-the-year-2040/'
response_code = requests.get(url)
soup = bs(response_code.text, 'html.parser')
all_texts = soup.find("div",class_="td-post-content tagdiv-type").get_text(strip = True, separator='\n')
firstdata = all_texts.splitlines()
firstdata

with open('/content/merge_from_ofoct.txt', 'r', encoding='latin1') as stopwordsfile:
    # Read the contents of the file
    stopwords = stopwordsfile.read().lower()
    stopWordList = stopwords.split('\n')
    stopWordList

with open('/content/positive-words.txt', 'r', encoding='latin1') as poswordsfile:
    # Read the contents of the file
    poswords = poswordsfile.read().lower()
positiveWordList=poswords.split('\n')

with open('/content/negative-words.txt', 'r', encoding='latin1') as negwordsfile:
    # Read the contents of the file
    negwords = negwordsfile.read().lower()
negativeWordList=negwords.split('\n')

"""# Cleaning using Stop Words Lists

"""

import nltk
nltk.download('punkt')
global tokens
def tokenizer(data_list):
    # Initialize an empty list to store filtered tokens from all strings
    all_filtered_words = []

    # Tokenize each string in the list
    for text in data_list:
        # Tokenize the current string
        tokens = nltk.word_tokenize(text.lower())

        # Filter tokens using stop words list
        filtered_words = [token for token in tokens if token not in stopWordList]

        # Remove punctuation
        filtered_words = [word for word in filtered_words if word.isalnum()]

        # Append filtered words to the list of all filtered words
        all_filtered_words.extend(filtered_words)

    return all_filtered_words


filtered_tokens = tokenizer(firstdata)
print(filtered_tokens)

"""#Extracting Derived variables(Positive,Negative,Polaity and Subjective score )

1.   **Positive Score**: This score is calculated by assigning the value of +1 for each word if found in the Positive Dictionary and then adding up all the values

1.  **Negative Score**: This score is calculated by assigning the value of -1 for each word if found in the Negative Dictionary and then adding up all the values. We multiply the score with -1 so that the score is a positive number.
2.   **Polarity Score:** This is the score that determines if a given text is positive or negative in nature. It is calculated by using the formula:
Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)
Range is from -1 to +1

2.  **Subjectivity Score**: This is the score that determines if a given text is objective or subjective. It is calculated by using the formula:
Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
Range is from 0 to +1
"""

def Positive_score(filtered_tokens):
    posword = 0
    for token in filtered_tokens:
        if token in positiveWordList:
            posword += 1
    return posword

def Negative_score(data_list):
    negword = 0
    for token in data_list:
        if token in negativeWordList:
            negword += 1
    return negword

def Polarity_score (Positive_score , Negative_score) :
  return (Positive_score - Negative_score) / ((Positive_score + Negative_score) + 0.000001)

def Subjective_score(Positive_score, Negative_score, total_words):
    return (Positive_score + Negative_score) / (total_words + 0.000001)

"""# Analysis of Readability

1.   **Average Sentence Length** = the number of words / the number of sentences

2.   **Percentage of Complex words** = the number of complex words / the number of words

3.  **Fog Index** = 0.4 * (Average Sentence Length + Percentage of Complex words)
"""

from nltk.tokenize import sent_tokenize, word_tokenize

def AverageSentenceLength(data_list):

    data_list = ' '.join(data_list)
    Wordcount = len(word_tokenize(data_list))
    SentenceCount = len(sent_tokenize(data_list))
    if SentenceCount > 0:
        Average_Sentence_Length = Wordcount / SentenceCount
    else:
        Average_Sentence_Length = 0  # Handle the case where there are no sentence

    return round(Average_Sentence_Length)

# Combine the lines into a single string


# Example usage:
AverageSentenceLength(firstdata)

def complex_word_percentage(data_list):
    data_list = ' '.join(data_list)
    # Assuming tokenizer is defined elsewhere to tokenize the data_list
    tokens = tokenizer(data_list)
    complexWord = 0

    for word in tokens:
        vowels = sum(1 for char in word if char.lower() in 'aeiou')  # Count vowels
        if not word.endswith(('es', 'ed')):
            if vowels > 2:
                complexWord += 1
        ComplexWordPercentage = complexWord/len(tokens)
    return ComplexWordPercentage  # Corrected variable name to return the count of complex words


complex_word_percentage(firstdata)

def fog_index(Average_Sentence_Length, complex_word_percentage):
    fogIndex = 0.4 * (Average_Sentence_Length + complex_word_percentage)
    return fogIndex

"""# Average Number of Words Per Sentence

**Average Number of Words Per Sentence** = the total number of words / the total number of sentences
"""

def average_words_per_sentence(text):
    text = ' '.join(text)
    # Split the text into sentences using simple splitting based on common punctuation marks
    sentences = [sentence.strip() for sentence in text.split('.') if sentence.strip()]  # Split on period (.), assuming sentences end with period

    # Calculate the total number of words in the entire text
    words = text.split()  # Split text into words based on whitespace
    total_words = len(words)

    # Calculate the total number of sentences
    total_sentences = len(sentences)

    # Calculate the average number of words per sentence
    if total_sentences > 0:
        average_words_per_sentence = total_words / total_sentences
    else:
        average_words_per_sentence = 0  # Handle division by zero if there are no sentences

    return average_words_per_sentence


avg_words_per_sentence = average_words_per_sentence(firstdata)
print("Average words per sentence:", avg_words_per_sentence)

"""# Complex Word Count

Complex words are words in the text that contain more than two syllables.
"""

def complex_word_count(data_list):
    # Assuming tokenizer is defined elsewhere to tokenize the data_list
    tokens = tokenizer(data_list)
    complexWord = 0

    for word in tokens:
        vowels = sum(1 for char in word if char.lower() in 'aeiou')  # Count vowels
        if vowels > 2:
          complexWord += 1
    return complexWord  # Corrected variable name to return the count of complex words


complex_word_count(firstdata)

"""# Word Count
counting total cleaned words present in the text by
removing the stop words (using stopwords class of nltk package).
removing any punctuations like ? ! , . from the word before counting.

"""

def filteredwords_count(data_list):
  all_filtered_words = []

  for text in data_list:
    # Tokenize the current string
    tokens = nltk.word_tokenize(text.lower())

    # Filter tokens using stop words list
    filtered_words = [token for token in tokens if token not in stopWordList]

    # Remove punctuation
    filtered_words = [word for word in filtered_words if word.isalnum()]

    # Append filtered words to the list of all filtered words
    all_filtered_words.extend(filtered_words)
    filteredwordcount = len(all_filtered_words)

  return filteredwordcount

filteredwords_count(firstdata)

"""# Personal Pronouns
To calculate Personal Pronouns mentioned in the text, we use regex to find the counts of the words - “I,” “we,” “my,” “ours,” and “us”. Special care is taken so that the country name US is not included in the list.
"""

def count_personal_pronouns(text):
    text = ' '.join(text)
    # Convert the text to lowercase for case-insensitive matching
    text_lower = text.lower()

    # Define the list of personal pronouns
    personal_pronouns = ["i", "we", "my", "ours", "us"]

    # Initialize counts dictionary
    counts = {pronoun: 0 for pronoun in personal_pronouns}

    # Split the text into words
    words = text_lower.split()

    # Count the occurrences of personal pronouns
    for word in words:
        # Exclude the word "us" if it's part of a country name like "US"
        if word == 'us' and not ('u.s.' in text_lower or 'united states' in text_lower):
            continue

        # Increment the count for the pronoun if it matches any personal pronoun
        if word in personal_pronouns:
            counts[word] += 1
            result = len(counts)

    return result

count_personal_pronouns(firstdata)

"""# Average Word Length
**Average Word Length is calculated by the formula:**
Sum of the total number of characters in each word/Total number of words

"""

def average_word_length(text):
    text = ' '.join(text)
    # Split the text into words
    words = text.split()

    # Calculate the total number of characters in all words
    total_characters = sum(len(word) for word in words)

    # Calculate the total number of words
    total_words = len(words)

    # Calculate the average word length
    if total_words > 0:
        average_length = total_characters / total_words
    else:
        average_length = 0

    return average_length


average_len = average_word_length(firstdata)
print(average_len)

import requests
from bs4 import BeautifulSoup
import pandas as pd

URLS = data['URL']
corps = []
article_titles=[]

# Filter out URLs that don't result in a 404 error
URLS = [url for url in URLS if requests.head(url).status_code != 404]

for url in URLS:
    try:
        response = requests.get(url, headers={"User-Agent": "XY"})
        response.raise_for_status()  # Raise an exception for other HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        article_title = soup.find('title').text
        article_titles.append(article_title)

        # Get article text
        text = soup.find(attrs={'class': 'td-post-content'}).get_text(strip = True, separator='\n')
        corps.append(text)

    except Exception as e:
        print(f"Error processing URL {url}: {e}")

# Create DataFrame
final = pd.DataFrame({'title': article_titles, 'corps': corps})

def tokenizer(text):
    tokens = nltk.word_tokenize(text.lower())
    filtered_words = [token for token in tokens if token not in stopWordList]
    filtered_words = [word for word in filtered_words if word.isalnum()]
    return filtered_words

final['filtered_tokens'] = final['corps'].apply(tokenizer)
final['URL'] = URLS
final['Positive_Score'] = final['filtered_tokens'].apply(Positive_score)
final['Negative_Score'] = final['filtered_tokens'].apply(Negative_score)
final['Polarity_score'] =  np.vectorize(Polarity_score)(final['Positive_Score'],final['Negative_Score'])
final['Subjective_Score'] = final.apply(lambda row: Subjective_score(row['Positive_Score'], row['Negative_Score'], len(row['filtered_tokens'])), axis=1)
final['Average_Sentence_Length'] = final['corps'].apply(AverageSentenceLength)
final['Complex_Word_Percentage'] = final['filtered_tokens'].apply(complex_word_percentage)
final['Fog_Index'] = np.vectorize(Polarity_score)(final['Average_Sentence_Length'],final['Complex_Word_Percentage'])
final['Average_Words_Per_Sentence'] = final['corps'].apply(average_words_per_sentence)
final['Complex_Word_Count'] = final['corps'].apply(complex_word_count)
final['Words_Count'] = final['corps'].apply(filteredwords_count)
final['Personal_Pronouns'] = final['corps'].apply(count_personal_pronouns)
final['Average_Word_Length'] = final['filtered_tokens'].apply(average_word_length)

final.drop(['filtered_tokens','corps'],axis = 1)

final.to_excel('Output Data Structure.xlsx')

