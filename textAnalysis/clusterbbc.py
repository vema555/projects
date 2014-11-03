import sys
import pandas
sys.path.append("../lib")
from bbcutils import load_market_matrix , load_terms_dict, load_classes
from gensim import corpora, models, matutils
from sklearn.cluster import KMeans

"""
(o) Load the bbc data set
(o) Convert the data into a gensim corpus format 
(o) Fintfd the TFIDF representation
(o) Perform the k-means clustering
"""
class DocClust:
    def __init__(self):
        self.bbc_data = load_market_matrix()
        self.trmdict = load_terms_dict()
        self.clstbl = load_classes()
        self.num_docs = len(self.clstbl)
        self.num_terms  = len(self.trmdict)
        self.clsdict = {0:"business",1:"entertainment",2:"politics",3:"sport",4:"tech"}

    def convert_format(self):
        docgrp = self.bbc_data.groupby("docid")
        corpus = [[] for  i in range(self.num_docs)]
        hdr = ["termid", "freq"]
        for name, group in docgrp:
            #print name, self.num_docs
            corpus[name] = list(group[hdr].itertuples(index=False))
        self.tfidf = models.TfidfModel(corpus)[corpus]
        print type(self.tfidf)

    def perform_kmeans(self):
        print self.num_terms, self.num_docs
        tfidfmat = matutils.corpus2dense(self.tfidf, self.num_terms, self.num_docs) 
        print "Perform K-means clustering"
        cluster_model = KMeans(n_clusters=5, init='k-means++', n_init=10, max_iter=300)
        self.labels = cluster_model.fit_predict(tfidfmat)
        
    def find_most_freqTerms_class(self):

    def join_with_docid(self):
        """ Joining the mmtx with the class table"""
        hdr =  ["termid",  "docid",  "tfidf", "classid"]
        self.tfidf_cls =  pandas.merge(self.tfidf_mat, self.clstbl, on="docid", how="outer").dropna()[hdr].sort(["termid", "docid"])
 
                

D = DocClust()
D.convert_format()
D.perform_kmeans()
