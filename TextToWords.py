#This class fetches words from text. It ignores non-alphabetic characters.

import re

class TextToWords:
	def __init__(self, filename, minlength=1, verbose=False):
		self.filename = filename
		self.minlength = minlength
		self.words = {}
		self.words_unique = []
		self.letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		print("Class",self.__class__.__name__,":: Instance created with",self.filename+".") if verbose else ""
	### END __init__ ###

	def isalpha(self,w):
		for ch in w:
			if ch not in self.letters:
				return(False)
		return(True)
	### END isalpha ###

	def detectWords(self):
		f = open(self.filename,'r')
		for line in f.readlines():
			#print(line)
			#words = re.findall(r'\w+', line.lower())
			###self.words += [word for word in re.findall(r'\w+', line.lower()) if self.isalpha(word)]#word.isalpha()]
			for word in re.findall(r'\w+', line.lower()):
				#Check if word contains only alphabets and follows length cutoff
				if self.isalpha(word) and len(word) >= self.minlength:#word.isalpha()]
					if word not in self.words:
						self.words[word] = 0
					self.words[word] += 1

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

