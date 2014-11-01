import pandas

def toInt(x):
	return int(x)

def toFloat(x):
	return float(x)

def load_market_matrix():
	""" Loading the market matrix file """
	fnm = "/Users/vema//Documents/kmeansml/bbc.mtx"
 	converters = {"termid": toInt, "docid": toInt, "freq":toFloat}
 	
 	X = pandas.read_table(fnm, header=None, sep=" ", skiprows=2, names= ["termid", "docid", "freq"], converters=converters)
 	X["termid"] = X["termid"] - 1
	X["docid"] = X["docid"] - 1
	return X


def load_terms_dict():
 	""" Loading the terms file """
 	fnm = "/Users/vema//Documents/kmeansml/bbc.terms"
 	term_dict = {}
 	with open(fnm, "r") as f:
 		for wordid, line in enumerate(f.readlines()):
 			word = line.strip()
 			term_dict[word] = wordid
  	return term_dict

def load_classes():
 	""" Loading the terms file """
 	fnm = "/Users/vema/Documents/kmeansml/bbc.classes"
 	converters = { "docid": toInt, "docid":toInt}
 	X = pandas.read_table(fnm, header=None, sep=" ", comment="%",  names= ["docid", "classid"], converters=converters)
 	return X





if __name__ == "__main__":
	mmtx = load_market_matrix()
	trmdict = load_terms_dict()
	clstbl = load_classes()
	

	print mmtx.tail()
	print clstbl.head()
	print clstbl.tail()	

	clsdict = {}
	for i, row in clstbl.iterrows():
		#print i,row["docid"] ,row["classid"]
		clsdict[row["docid"]] = row["classid"]

	#arr = []
	#for i, row in mmtx.iterrows():
    #		dcid = row["docid"]
	#	#print row
	#	arr.append( clsdict[dcid])
	#mmtx["clsid2"] = arr
	#X =  clstbl.join( mmtx, on="docid", how="outer", lsuffix=".x", rsuffix=".y").dropna()
	#mmtx2 = mmtx.tail(100)
	hdr = ["termid",  "docid",  "freq", "classid"]
	#X = mmtx2.join( clstbl, on="docid", how="outer", lsuffix=".x", rsuffix=".y").dropna()[hdr].sort(["termid", "docid"])
	X = pandas.merge(mmtx, clstbl, on="docid", how="outer").dropna()[hdr].sort(["termid", "docid"])

	#print len(X)
	#print X.head()
	print X.to_string()
	#print mmtx2.to_string()
	print len(mmtx)
	print len(X)