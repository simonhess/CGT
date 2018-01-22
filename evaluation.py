# -*- coding: utf-8 -*-
# import modules & set up logging
import PreProcessor
import numpy as np
from Definitions import ROOT_DIR
import os, PreProcessor
from InferSent.encoder.infersent import InferSent
from code import Code
import sent2vec.sent2vec_encoder
import time

os.chdir(ROOT_DIR)

papers = PreProcessor.csvimport()
codes = PreProcessor.code_to_list()

numberOfPapers = len(papers)

vocabulary = {}
vocabulary = set()

#Build vocabulary from codes und papers
for code in codes:
    vocabulary.update(code.cleared_code.split())

numberOfSentences = 0

for paper in papers:
    numberOfSentences += len(paper.cleared_paper)
    for line in paper.cleared_paper:
        vocabulary.update(line.split())

vocabulary = list(vocabulary)

print("Codes " + str(len(codes)))
print("sents " + str(numberOfSentences))

numberOfScores = len(codes) * numberOfSentences


#infersentEncoder = InferSent(vocabulary=vocabulary)


def get_infersent_score():

    score = np.zeros(shape=(numberOfScores, 4))

    print(score.shape)

    infersentEncoder = InferSent(vocabulary=vocabulary)

    # Get code embeddings
    codelist = []
    for code in codes:
        codelist.append(code.cleared_code)
    code_embeddings = infersentEncoder.get_sent_embeddings(codelist)
    for i in range(len(codes)):
        codes[i].embedding = code_embeddings[i]

    index = 0

    start_time = time.time()

    for paper in papers:
        print("Encoding paper " + str(paper.id) + " / "+ str(numberOfPapers))
        paper_embeddings = infersentEncoder.get_sent_embeddings(paper.cleared_paper)
        for sentence_id in range(len(paper.cleared_paper)):
            for code in codes:
                score[index, 0] = paper.id
                score[index, 1] = sentence_id
                score[index, 2] = code.id
                score[index, 3] = infersentEncoder.cosine(code.embedding,paper_embeddings[sentence_id])
                index += 1

        print("--- %s seconds ---" % (time.time() - start_time))

    os.chdir(ROOT_DIR)
    #np.savetxt("score.csv", score, delimiter=";", fmt='%1.3f')
    #csv = np.genfromtxt('score.csv', delimiter=";")
    np.save('infersent_score.npy', score)

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

def get_infersent_score2():

    score = np.zeros(shape=(numberOfScores, 4))

    print(score.shape)

    infersentEncoder = InferSent(vocabulary=vocabulary)

    # Get code embeddings
    codelist = []
    for code in codes:
        codelist.append(code.cleared_code)
    code_embeddings = infersentEncoder.get_sent_embeddings(codelist)
    for i in range(len(codes)):
        codes[i].embedding = code_embeddings[i]

    index = 0
    papercount = 0

    start_time = time.time()

    #infersentEncoder = None

    for paper in papers:

        print("Encoding paper " + str(paper.id) + " / "+ str(numberOfPapers))
        sent_embedding = np.zeros(shape=(0,4096))
        sent_chunks = chunks(paper.cleared_paper, 5)
        for chunk in sent_chunks:
            #print(chunk)
            chunk_embedding = infersentEncoder.get_sent_embeddings(chunk)
            #print(chunk_embedding.shape)
            sent_embedding = np.vstack((sent_embedding,chunk_embedding))
        #sent_embedding = infersentEncoder.get_sent_embeddings([paper.cleared_paper[sentence_id]])

        for sentence_id in range(len(paper.cleared_paper)):
            for code in codes:
                score[index, 0] = paper.id
                score[index, 1] = sentence_id
                score[index, 2] = code.id
                score[index, 3] = infersentEncoder.cosine(code.embedding,sent_embedding[sentence_id])
                index += 1

        print("--- %s seconds ---" % (time.time() - start_time))

    os.chdir(ROOT_DIR)
    #np.savetxt("score.csv", score, delimiter=";", fmt='%1.3f')
    #csv = np.genfromtxt('score.csv', delimiter=";")
    np.save('infersent_score.npy', score)

def get_sent2vec_score():

    score = np.zeros(shape=(numberOfScores, 4))

    print(score.shape)

    # Get code embeddings
    codelist = []
    for code in codes:
        codelist.append(code.cleared_code)
    #code_embeddings = sent2vec.sent2vec_encoder.get_sentence_embeddings(codelist, ngram='unigrams', model='toronto')
    code_embeddings = sent2vec.sent2vec_encoder.encode(codelist)
    for i in range(len(codes)):
        codes[i].embedding = code_embeddings[i]

    index = 0

    start_time = time.time()

    for paper in papers:
        print("Encoding paper id " + str(paper.id))
        #paper_embeddings = sent2vec.sent2vec_encoder.get_sentence_embeddings(paper.cleared_paper, ngram='unigrams', model='toronto')
        paper_embeddings = sent2vec.sent2vec_encoder.encode(paper.cleared_paper)
        for sentence_id in range(len(paper.cleared_paper)):
            for code in codes:
                score[index, 0] = paper.id
                score[index, 1] = sentence_id
                score[index, 2] = code.id
                score[index, 3] = sent2vec.sent2vec_encoder.cosine(code.embedding, paper_embeddings[sentence_id])
                #print(paper.cleared_paper[int(score[index, 1])] + " // " + codes[int(score[index, 2])].cleared_code + " //// " + str(score[index, 3]))
                index += 1
        print("--- %s seconds ---" % (time.time() - start_time))


    #sents = []
    #sents.append('our finding suggest that the analysis of mouse cursor movement may enable researcher to assess negative emotional reaction during live system use examine emotional reaction with more temporal precision conduct multimethod emotion research and provide researcher and system designer with an easy to deploy but powerful tool to infer user negative emotion to create more unobtrusive affective and adaptive system')
    #sents.append('the value of automatically analyze external datum')
    #embeddings = sent2vec.sent2vec_encoder.get_sentence_embeddings(sents, ngram='unigrams', model='toronto')
    #print(sent2vec.sent2vec_encoder.cosine(embeddings[0],embeddings[1]))

    os.chdir(ROOT_DIR)
    #np.savetxt("score.csv", score, delimiter=";", fmt='%1.3f')
    np.save('sent2vec_score.npy', score)

def get_evaluation_samples():
    score = np.load('sent2vec_score.npy')
    score = np.nan_to_num(score)
    print(score[0,:])
    print(score[1, :])
    print(np.argwhere(np.isnan(score)))
    print(len(np.argwhere(np.isnan(score))))
    #print(score[19085570, :])
    #print(score[23199679, :])

    # print(np.percentile(score, 90, axis=0, interpolation='lower')[3])
    # print(np.percentile(score, 80, axis=0, interpolation='lower')[3])
    # print(np.percentile(score, 70, axis=0, interpolation='lower')[3])
    # print(np.percentile(score, 60, axis=0, interpolation='lower')[3])
    # print(np.percentile(score, 50, axis=0, interpolation='lower')[3])
    # print(np.percentile(score, 40, axis=0, interpolation='lower')[3])
    # print(np.percentile(score, 30, axis=0, interpolation='lower')[3])
    # print(np.percentile(score, 20, axis=0, interpolation='lower')[3])
    # print(np.percentile(score, 10, axis=0, interpolation='lower')[3])

#get_evaluation_samples()
#get_sent2vec_score()
#get_infersent_score()

