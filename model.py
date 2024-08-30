# Data preprocessing libraries
import nltk
import pandas as pd
import re
# print('imported processors')

# Data visualisation libraries
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
# print('imported pandas')

# Latent Semantic Analysis libraries
from scipy.sparse.linalg import svds
# print('imported sematic analysis')

import torch
# Bert Summarizer model
from summarizer import Summarizer
# print('imported bert')




# Main Function


def summarize(text):

    # # Extracting text from 'file.txt' 
    # with open('file.txt', 'r') as file:
    #     text = file.read()
    
    # if mtext == False:
    #     text = jtext
    # elif jtext == False:
    #     text = mtext
    # # print(text)


    # Removing new line characters and double spaces and then rejoining the rest of the text
    text = re.sub(r'\n|\r', ' ', text)
    text = re.sub(r' +', ' ', text)
    text = text.strip()
    # print('done processing')

    # The number of words changes should not change too much

    # Let's check the number of words in new text
    print('The number of words in the text is:',len(text))

    # Tokenization to check the number of sentences in the document
    # The number of sentences in 'text'
    sentences = nltk.sent_tokenize(text)
    print('The number of sentences in the document now is:', len(sentences))


    # EXPLORATION AND PREPROCESSING
    # Creating a variable for stopword in English such as the, an, in, a, that take up processing time unnecessarily
    # NLTK library has a list of stopwords that we will use

    stop_words = nltk.corpus.stopwords.words('english')

    def normalize_document(doc):
        # lower case and remove special characters\whitespaces
        doc = re.sub(r'[^a-zA-Z\s]', '', doc, re.I|re.A)
        doc = doc.lower()
        doc = doc.strip()
        
        # tokenize document
        tokens = nltk.word_tokenize(doc)
        
        # filter stopwords out of document
        filtered_tokens = [token for token in tokens if token not in stop_words]
        
        # re-create document from filtered tokens
        doc = ' '.join(filtered_tokens)
        return doc

    # Vectorizing the document
    normalize_corpus = np.vectorize(normalize_document)

    # Normalizing the sentences
    norm_sentences = normalize_corpus(sentences)
    norm_sentences[:3]

    # Converting text data to vectors, textual data into numerical data
    tv = TfidfVectorizer(min_df=0., max_df=1., use_idf=True)

    # Creating the document term matrix, which shows us the number of documents( in our case sentences), and the number of distinct words in them

    dt_matrix = tv.fit_transform(norm_sentences)
    dt_matrix = dt_matrix.toarray()

    vocab = tv.get_feature_names_out()
    td_matrix = dt_matrix.T
    print('The dimension of term document matrix or (terms, sentences) is:', td_matrix.shape)
    pd.DataFrame(np.round(td_matrix, 2), index=vocab).head(10)

    # Defining variables for u, s and vt and creating the SVD matrix  
    def low_rank_svd(matrix, singular_count=2):
        u, s, vt = svds(matrix, k=singular_count)
        return u, s, vt

    # modelling part 
    num_sentences = 8
    num_topics = 3

    u, s, vt = low_rank_svd(td_matrix, singular_count=num_topics)  
    print(u.shape, s.shape, vt.shape)
    term_topic_mat, singular_values, topic_document_mat = u, s, vt

    # remove singular values below threshold                                         
    sv_threshold = 0.5
    min_sigma_value = max(singular_values) * sv_threshold
    singular_values[singular_values < min_sigma_value] = 0

    salience_scores = np.sqrt(np.dot(np.square(singular_values), 
                                    np.square(topic_document_mat)))

    top_sentence_indices = (-salience_scores).argsort()[:num_sentences]
    top_sentence_indices.sort()

    # print(text)
    print("The number of words in the 'text' is:", len(text))

    # Summarize the text with bert

    result = Summarizer()(text, min_length = 50)
    summary_bert = ''.join(result)

    # Writing the summary in 'summary.txt' file
    f_summary = open("summary.txt", "a")
    f_summary.write(summary_bert)
    f_summary.close()

    return 'checking'

if __name__ == '__main__':
    summarize()