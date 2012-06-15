# -*- coding: utf-8 -*-
# Johanna Mohlin & Sofi M Belfrage

import re
import snigl


class Composer(object):
	""" Class Composer is used to analyze compositions"""
	
	def __init__(self, inputCorpus, lexicon, frequencyDict):

		data = unicode(open("../resources/8sidor_sammans.txt").read(), "utf8")
		
		newData = re.sub(r'\s+|\d+', " ", data)	# Removes all extra whitespaces and digits and replaces them with one space
		self.compList = newData.split()				# The compositionfile 8sidor_sammans.txt is split into words on whitespaces
		self.lexicon = lexicon
		self.largeCorpus = self.compList + [x for x,y in inputCorpus] # The list will only contain the lexem-form
		self.corpus = inputCorpus
		self.freq = frequencyDict

	def composition(self, lexem):
		""" The Function composition() takes one argument,
		 		a lexem that is thought to be a composition,
				it devides it into meningfull parts and finds
				the matching image/images filename.
				Returns a list of filenames."""
				
		if len(lexem) < 6: return ["UNKNOWN"]						# Only words with six or more letters will be analyzed
				 
		listOfLexem = [] 							# This list will contain the compositions parts as lexems
	
		if lexem in self.compList:							# if the lexem is already in the file (the simplest case)
			division = self.compList.index(lexem) + 1 		# the division of the lexem is on the index just after the lexem
			listOfLexem = self.compList[division].split("~")	# Split the division on the "~"-sign and it becomes the listOfLexem


		else:											
			num2 = len(lexem)							# Otherwise the program looks at one character at the time from the end
			num = num2 - 3								#   of the word and tries to find lexems that are in the file to match with
			checkCorpus = self.largeCorpus				# the largeCorpus is the tagged corpus plus the composition-file
			while (num >= 0):							# Finds the a lexem longer than 2 characters from the end, then finds more lexems
				lexemEnding = lexem[num : num2]
				if lexemEnding in checkCorpus:
					listOfLexem.insert(0,lexemEnding)
					num2 = num
					num -= 3			
					checkCorpus = self.largeCorpus
				else:
					num -= 1
					checkCorpus = [x for x in checkCorpus if lexemEnding == x[len(lexemEnding)*-1:]]	

			
		listOfLexem = [x for x in listOfLexem if len(x) > 1]
		
		
		if listOfLexem == []:						# If the listOflexem is empty after the first check, it tries to find some kind of
			checkCorpus = self.largeCorpus			#  substring with 3 characters or more
			for word in checkCorpus :
				if word in lexem :
					if len(word) >= 3 :
						listOfLexem.append(word)
						lexem = lexem.replace(word,'|')
		
		
		def findWord(input):
			""" Function findWord() takes a lexem and finds the most frequent lemma and returns it"""
			
			val = snigl.disambiguate(input, self.freq, self.corpus )
			return val[0] if val else "UNKNOWN"
			
		listOfLemma = [findWord(x) for x in listOfLexem]		# listOfLexem is transformed into a list of lemmas 
		output = snigl.getImage(listOfLemma, self.lexicon)		# Calls the function getImage from module snigl and returns list of blisssymbol filenamnes
		output = [x for x in output if x != "UNKNOWN"]
		return output if len(output) > 0 else ["UNKNOWN"]
		
			

if __name__ == '__main__':
	lex = snigl.getLexicon()
	corpus = snigl.tokenizeCorpus()
	symbol_freq_dist, lemma_freq_dist = snigl.getFreq(corpus) 
	comper = Composer(corpus, lex, lemma_freq_dist)
	
	
	print comper.composition(u"bilstol") # funkar ej (lemma-formen dyker sällan upp i korpuset. 
	print comper.composition(u"bilstolar") # funkar
	

