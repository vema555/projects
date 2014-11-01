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
 			term_dict[wordid] = word
  	return term_dict

def load_classes():
 	""" Loading the terms file """
 	fnm = "/Users/vema/Documents/kmeansml/bbc.classes"
 	converters = { "docid": toInt, "docid":toInt}
 	X = pandas.read_table(fnm, header=None, sep=" ", comment="%",  names= ["docid", "classid"], converters=converters)
 	return X

