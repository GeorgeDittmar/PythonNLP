from __future__ import division
import re
class HMM:
	def __init__(self,training):
		self.words = {}
		self.word_counts = {}
		self.ngrams = {1:{},2:{},3:{}}
		
		# training is an open file that we loop over line by line.
		for line in training:
			tokens = line.strip().split()
			counts = int(tokens[0])
			key = tuple(tokens[2:])
			
			if tokens[1] == '1-GRAM': 
				self.ngrams[1][key[0]] = counts
			if tokens[1] == '2-GRAM': self.ngrams[2][key] = counts
			if tokens[1] == '3-GRAM': self.ngrams[3][key] = counts
			if tokens[1] == 'WORDTAG': 
				self.words[key] = counts
				self.word_counts.setdefault(key[1],0)
				self.word_counts[key[1]] += counts
			
	# returns the total count of a given word
	def getWordCounts(self,word):
		return self.word_counts.get(word,0.0)
		
	# returns the total count of the word with a given tag in the data set.
	def getWordTagCount(self,word,tag):
		return self.words.get((tag,word),0.0)
	
	def replace_word(self,word):
		regex = '[0-9]'
		lowerCaseRegex = '/[a-z]/'
		digitP = re.compile(regex)
		lowerReg = re.compile(lowerCaseRegex)
		if self.word_counts.get(word,0.0) < 5:
			if digitP.match(word):
				return "_Numeric_"
			elif lowerReg.match(word) == None:
				return "_AllUpper_"
			elif word[len(word)-1].isUpper():
				return "_LastUpper_"
			return "_RARE_"
		else: return word
	
	def getTags(self):
		return self.ngrams[1].keys()
	
	def e(self, x,y):
		if y in ["*","STOP"]: return 0.0
		else: 
			replaced = self.replace_word(x)
			return self.getWordTagCount(replaced,y) / self.ngrams[1][y]

	def trigram_prob(self,tri):
		bigram = tri[:-1]
		prob = self.ngrams[3].get(tri,0.0)/self.ngrams[2][bigram]
		return prob
