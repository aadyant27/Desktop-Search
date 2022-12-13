import os
import textract
import re
import nltk

# Stopwords
from nltk.corpus import stopwords
nltk.download('stopwords')
stopword = stopwords.words('english')
# print(stopword)


# This function filters words(string of word) if,
# 1. If the string start with space OR
# 2. If string consists of more than 1 word OR
# 3. If string contains less than 1 characters i.e. single letters or empty strings OR
# 4. (by this step only single words in the string remain), If word(in string) is one of the STOPWORDS
def filter_words(word):
    if re.search('^ ', word) or len(word.split()) > 1 or len(word) <= 1 or word in stopword:
        return False
    else:
        return True


def pdf_reader(path):
    text = textract.process(path, method='pdftotext')
    # Decode() is used to convert 'byte' string which we get from 'textextract' method to 'character' string.
    text = text.decode().split()
    all_words = []
    for i in text:
        # To filter out words which does not consists of letters i.e. replacing non-alphabetic char. with ' '.
        temp = re.sub('[^a-zA-Z]', ' ', i)
        # To remove any trailing or leading zeros in the word
        temp = temp.strip()
        # To make all words lowercase
        temp = temp.lower()
        all_words.append(temp)

    # Filtering words in the list based on some conditions
    filtered_words = list(filter(filter_words, all_words))
    # print(filtered_words)
    return filtered_words
# ///////////////////////////////////////////////////////////////////////////////////


# For Docx
def docx_reader(path):
    text = textract.process(path).decode()
    text = text.split()

    all_words = []
    for i in text:
        # Replacing every non-alphabetic character with a space
        temp = re.sub('[^a-zA-Z]', ' ', i)
        temp = temp.strip().lower()
        all_words.append(temp)
    filtered_words = list(filter(filter_words, all_words))
    print(filtered_words)
# //////////////////////////////////////////////////////////////////////////////////


# For Txt
def text(path):
    pass

# /////////////////////////////////////////////////////////////////////////////////


