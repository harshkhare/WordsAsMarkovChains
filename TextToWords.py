#This class fetches words from text. It ignores non-alphabetic characters.

import re

class TextToWords:
	def __init__(self, filename, minlength=1, verbose=False):
		self.filename = filename
		self.minlength = minlength
		self.words = {}
		self.words_unique = []
		self.letters = ["'",'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		print("Class",self.__class__.__name__,":: Instance created with",self.filename+".") if verbose else ""
	### END __init__ ###

	def isalpha(self,w):
		for ch in w:
			if ch not in self.letters:
				return(False)
		return(True)
	### END isalpha ###

	def detectWords(self,apostrophe=False,ignoreUpperCase=False):
		f = open(self.filename,'r')
		for line in f.readlines():
			#print(line)
			#words = re.findall(r'\w+', line.lower())
			###self.words += [word for word in re.findall(r'\w+', line.lower()) if self.isalpha(word)]#word.isalpha()]

			if apostrophe:
				p = re.compile(r'\w+\'?\w+') # Use this for words with apostrophes.
			else:
				p = re.compile(r'\w+') # Use this for words without apostrophes (words will be split by apostrophe).

			for word in p.findall(line):
				#Check if word follows length cutoff and contains only alphabets and ignore upper case words if ignoreUpperCase is True.
				if len(word) >= self.minlength and self.isalpha(word) and not(ignoreUpperCase and sum(1 for c in word if c.isupper())>1):#word.isalpha()]
					if word not in self.words:
						self.words[word.lower()] = 0
					self.words[word.lower()] += 1

		#Filter words with length
		###self.words = [word for word in self.words if len(word) >= self.minlength]

		#Optional: Find unique words
		#self.words_unique = list(dict.fromkeys(self.words))

		#Print detected words
		#print(len(self.words),len(self.words_unique))
		#print(self.words)
	### END detectWords ###

	def aslist(self):
		return([list(w) for w in self.words.keys()])

###### END Class TextToWords ######
