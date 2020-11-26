import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer

def textSummarizationUsingRanking(txt):
    # From input tuple of words, we change 
    whole_text = readWholeText(txt)
    # Get corpus from whole text
    corpus, doc = getCorpus(whole_text)
    # 
    word_frequency = featureExtraction(whole_text, corpus)
    # 
    sorted_word_frequency = getRelativeFrequencyOfWords(word_frequency)
    # 
    sentences_ranking, top_sentences = getSentenceRanking(sorted_word_frequency, doc)
    # 
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
    val = sorted(frequency.values())
    print("Values: ")
    print(val)

    higher_word_frequency = [word for word, freq in frequency.items() if freq in val[-3:]]
    print("\nWords with higher frequencies: ")
    print(higher_word_frequency)
    
    higher_frequency = val[-1]
    for word in frequency.keys():
        frequency[word] = (frequency[word] / higher_frequency)
    return frequency

def getSentenceRanking(frequency, doc):
    sentence_rank = {}
    for sent in doc.sents:
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
    
    print(summary)
    summary_text = ""
    for i in summary:
        summary_text = summary_text + " " + str(i)
    
    print("\nSummary : " + summary_text)
    return summary_text