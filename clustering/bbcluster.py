import pandas
import numpy as np
from utils import load_market_matrix, load_terms_dict, load_classes

class DocClustering:
    def __init__(self):
        self.mmtx = load_market_matrix()
        self.trmdict = load_terms_dict()
        self.clstbl = load_classes()
        self.num_docs = len(self.clstbl)
        self.clsdict = {0:"business",1:"entertainment",2:"politics",3:"sport",4:"tech"}

    def calc_tf(self):
        """ Calculating the TF IDF of the document """
        groupby_document = self.mmtx.groupby("docid")
        subd = []
        for docid, docgrp  in groupby_document:
            maxfreq = docgrp.freq.max()
            docgrp["tf"] = docgrp["freq"]/maxfreq
            subd.append( docgrp )
        
        self.tf_mat = pandas.concat( subd) 
 
    def calc_idf(self):
        """ Calculating the Inverse DF of each word """
        groupby_termid = self.mmtx.groupby("termid")
        
        subd = []
        for termid, termgrp  in groupby_termid:
            sz = np.log(self.num_docs/float(len(termgrp)))
            subd.append( (termid, sz))
        
        self.idf_mat = pandas.DataFrame(subd, columns = ["termid", "idf"]) 
 
    def compute_tfidf(self):
        self.calc_tf()
        self.calc_idf()
        # Do a left outer join of the tables tf, idf two on termid
        hdr =  ["termid",  "docid",  "freq", "classid"]
        self.tfidf_mat =  pandas.merge(self.tf_mat, self.idf_mat, on="termid", how="outer").dropna().sort(["termid", "docid"])
        self.tfidf_mat["tfidf"] = self.tfidf_mat["tf"] * self.tfidf_mat["idf"]
        return self.tfidf_mat
  

    def join_with_docid(self):
        """ Joining the mmtx with the class table"""
        hdr =  ["termid",  "docid",  "tfidf", "classid"]
        self.tfidf_cls =  pandas.merge(self.tfidf_mat, self.clstbl, on="docid", how="outer").dropna()[hdr].sort(["termid", "docid"])
 

    def frequent_words_class(self):
        grouped = self.tfidf_cls.groupby(["termid", "classid"])
        data = []
        for name, group in grouped:
            dtup  = name + (group["tfidf"].sum(),)
            data.append(dtup)
        subdf = pandas.DataFrame(data, columns = ["termid", "classid", "tfidf"])
         
        classgrped = subdf.groupby("classid")
        for classid, group in classgrped:
            srtgrp = group.sort(["tfidf"], ascending=False)
            freqterms = srtgrp["termid"].head(10)
            for termid in freqterms:
                print classid, self.clsdict[classid], self.trmdict[termid]


if __name__ == "__main__":
    D = DocClustering()
    D.compute_tfidf()
    D.join_with_docid()
    D.frequent_words_class()
    #D.calc_tf()
    #D.compute_idf()

