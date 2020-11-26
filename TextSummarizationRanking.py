import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer

def textSummarizationUsingRanking(txt):
    # From input tuple of words, we change 
    whole_text = readWholeText(txt)
    # Get corpus from whole text
    corpus, doc = getCorpus(whole_text)
    # Count word frequency in text
    word_frequency = featureExtraction(whole_text, corpus)
    # Sort word frequency and get new value for word frequency (divided by highest freq)
    sorted_word_frequency = getRelativeFrequencyOfWords(word_frequency)
    # Set the sentence ranking and top score of sentence
    sentences_ranking, top_sentences = getSentenceRanking(sorted_word_frequency, doc)
    # Get the summarization
    summary = getSummaryText(sentences_ranking, top_sentences)

    return summary

def readWholeText(text):
    # Joining the text bcs the returned value is tuple
    whole_text = " ".join(text)
    return whole_text

def getCorpus(text):
    # Use the library
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    print(doc)

    # Lower case the text    
    corpus = [sent.text.lower() for sent in doc.sents]

    # Define the global variable
    global text_len
    text_len = 0
    # Count the text length
    for sent in doc.sents:
        text_len += len(sent)
    print("\nText length: ", text_len)

    return corpus, doc

def featureExtraction(text, corpus):
    # Clean the stop words
    cv = CountVectorizer(stop_words=list(STOP_WORDS))
    # Feature extraction
    cv_fit = cv.fit_transform(corpus)

    word_list = cv.get_feature_names()
    count_list = cv_fit.toarray().sum(axis=0)
    
    word_frequency = dict(zip(word_list, count_list))
    return word_frequency

def getRelativeFrequencyOfWords(frequency):
    # Sort the frequency value we got before
    val = sorted(frequency.values())
    print("Values: ")
    print(val)

    # Take word which the value is in top 3 highest value from the list
    higher_word_frequency = [word for word, freq in frequency.items() if freq in val[-3:]]
    print("\nWords with higher frequencies: ")
    print(higher_word_frequency)
    
    # Take the highest value from the list 
    higher_frequency = val[-1]
    for word in frequency.keys():
        # Update the value of each word in dictionary with new value
        frequency[word] = (frequency[word] / higher_frequency)
    return frequency

# Create sentence ranking from each word value
def getSentenceRanking(frequency, doc):
    sentence_rank = {}
    # For each sentence in text
    for sent in doc.sents:
        # For each word in sentence
        for word in sent:
            if word.text.lower() in frequency.keys():
                if sent in sentence_rank.keys():
                    sentence_rank[sent] += frequency[word.text.lower()]
                else:
                    sentence_rank[sent] = frequency[word.text.lower()]
            else:
                continue

    top_sentences = (sorted(sentence_rank.values())[::-1])
    top_sent = top_sentences[:3]
    print("\nTop sentences : ")
    print(top_sent)

    return sentence_rank, top_sent

def getSummaryText(rank, top_sent):
    summary = []
    for sent, strength in rank.items():
        if strength in top_sent:
            summary.append(sent)
        else:
            continue
    
    summary_text = ""
    sum_len = 0
    for i in summary:
        summary_text = summary_text + " " + str(i)
        sum_len += len(i)
    
    # text_reduced = sum_len / text_len*100
    # summary_text = summary_text + "\n\n" + "Text reduced to : " + str("{:.1f}%".format(text_reduced)) + " (" + str(sum_len) + "/" + str(text_len) + ")"
    summary_text = summary_text + "\n\n" + "Text reduced from : " +  str(text_len) + " words to " + str(sum_len)

    print("\nSummary : " + summary_text)
    print("\nSummary length : ", sum_len)
    return summary_text