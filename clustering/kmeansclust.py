#Om Namah Sivaya

import scipy.sparse as sps
from sklearn.cluster import Kmeans

def getTFIDF():
    from bbcluster import DocClustering
    D = DocClustering()
    return D.compute_tfidf()
      
class KmeansClust:

    def __init__(self):
        self.tfidf_tbl = getTFIDF()

    def convert2tf(self):
        pass


if __name__ == "__main__":
    S = getTFIDF()
    
    print S.tail()
    print len(S)
    rows = S["termid"].values
    cols = S["docid"].values
    Ssp_mat = sps.coo_matrix(S["tfidf"].values, (rows, cols))