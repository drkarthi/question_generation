import preprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdb
import networkx as nx
import operator

class sentence_node:
	def __init__(self,id,sentence):
		self.id = id
		self.sentence = sentence

def main():
	preprocess.main()
	nodes = []
	sentences = []
	with open('sentences.txt') as f:
		while(True):
			line = f.readline()
			if(line=='\n' or line==''):
				break
			nodes.append(sentence_node(0,line.strip('\n')))
	print len(nodes)
	for x in range(len(nodes)):
		sentences.append(nodes[x].sentence)
	tfidf_vectorizer = TfidfVectorizer()
	tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)
	similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
	G = nx.Graph()
	for x in range(len(nodes)):
		G.add_node(x)
	# G.add_nodes_from(nodes)
	for i in range(len(nodes)):
		for j in range(len(nodes)):
			if(i<j and similarity_matrix[i][j]!=0):
				G.add_edge(i,j,weight=similarity_matrix[i][j])
	pdb.set_trace()			
	for i in range(len(nodes)):
		if len(G[i]) == 0:
			print "No out edges"					
	pr = nx.pagerank(G,alpha=0.85)
	# print pr
	sorted_pr = sorted(pr.items(), key=operator.itemgetter(1), reverse=True)
	print sorted_pr[:10]
	for item in sorted_pr[:10]:
		print nodes[item[0]].sentence			

main()