from __future__ import division
from HMM import HMM

class Tagger:
	
	def __init__(self,genes):
		self.hmm = HMM(genes)
		
	# Calculates the emission probability of a given word tag pair
	def e(self,x,u):
		#x is the word y is the tag for the given word
		return self.hmm.e(x,u)
	
	def q(self,w,u,v):
		return self.hmm.trigram_prob((u,v,w))
																		
	# Find the argmax of all x's from the sentence input. We use the HMM.e(x|y) method to generate our list of values. 	
	def argmax(self,eminlist):
		return max(eminlist,key=lambda x : x[1])
		
	def calc(self,text,tags):
		wordTags = []
		
		# not very pythonic but works for now
		for tag in tags:
			wordTags.append((tag,self.e(text,tag)))
		return wordTags
	
	def k_val(self,k):
		if k in (-1,0): return ['*']
		else: return self.hmm.getTags()
	
	#Dynammic programming for the Viterbi algorithm
	def viterbi(self, sentence):
		n = len(sentence)
		
		x = [""]+sentence
		y = [""]*(n+1)
		
		pi = {}
		pi[0,'*',"*"] = 1
		back_pointers = {}
		
		for k in range(1,n+1):
			for u in self.k_val(k-1):
				for v in self.k_val(k):
					back_pointers[k,u,v],pi[k,u,v] = self.argmax([(tag,pi[k-1,tag,u] * self.q(v,tag,u)*self.e(x[k],v)) 
																                        for tag in self.k_val(k-2)])
							
		(y[n-1],y[n]),score = self.argmax([ ((u,v), pi[n,u,v] * self.q("STOP",u,v)) for u in self.k_val(n-1) for v in self.k_val(n)])
		
		for k in range((n-2),0,-1):
			y[k] = back_pointers[k+2,y[k+1],y[k+2]]
		y[0] = '*'
		tagScores = []
		for i in range(1,n):
			tagScores.append(pi[i,y[i-1],y[i]])
			
		return y[1:n+1],tagScores+[score]
		
	# reads in the gene data and returns each sentence of the document.
	def read_sent(self,data):
		sentence = []
		
		for word in data:
			if word.strip():
				sentence.append(word.strip())
			else:
				yield sentence
				sentence = []

	def print_tags(self,sentence,tags):
		print "\n".join([word+" "+tag for word,tag in zip(sentence,tags[0])])

	
gene_counts = open("gene.counts.new")
gene_test = open("gene.test")
gene_test2 = open("gene.dev")
tagger = Tagger(gene_counts)
tags = tagger.hmm.getTags()

# grab each sentence and process to calc the gene tags	
for sentence in tagger.read_sent(gene_test2):
	y = tagger.viterbi(sentence)
	tagger.print_tags(sentence, y)
	print


"""
for word in gene_test:)
	if word in ['\n','\r\n']:
		print
	else:
		tagScores = tagger.calc(word.strip(),tags)
		print word.strip(), tagger.argmax(tagScores)[0][0]	
"""

	
	
