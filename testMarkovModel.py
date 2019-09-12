#Generate statistics for performance of the markov model

from TextToWords import TextToWords
from MarkovModel import MarkovModel


#datafile = "data/data_wiki_earth.txt"
datafile = "data/WebOfScience_abstracts.txt"

minlen = 2
states = ['^','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
numWords = 5000 #Words to be generated for calculation of statistic
apostropheFlag = False
ignoreUpperCaseFlag = True

t2w = TextToWords(datafile,minlength=minlen)
t2w.detectWords(apostrophe=apostropheFlag, ignoreUpperCase=ignoreUpperCaseFlag)
#print(t2w.words)
#print(t2w.aslist())
words_as_lists = t2w.aslist()


###############################################################################################

print("\n-----------------------------------------------------------------------------")
print("Data:",datafile)
print("Minumum word length =",minlen)
print("Total number of words =",len(t2w.words))
print("Number of words to be generated for calculation of statistic =",numWords)
print("-----------------------------------------------------------------------------\n")

###############################################################################################

print("Word length histogram\nLength Count")
for l in range(1,21):
	print(l,len([w for w in words_as_lists if len(w)==l]))
print("\n-----------------------------------------------------------------------------\n")

###############################################################################################

print("Statistics for models trained with all words.")
print("One model for each order.\n")
print("\tWord Length")
print("Order\t2\t3\t4\t5\t6\t7")
for order in [1,2,3]:
	print(order,end="\t")
	model = MarkovModel()

	#Fit model to input data and write to file.
	model.fit(state_sequences=words_as_lists, states=states, order=order)
	#model.tofile(filename="WebOfScience_abstracts_order-"+str(order)+"_wordLength-all.bin")

	#Load model from file. Do not write to file.
	#model.fit(filename="data_WebOfScience_abstracts_order-1_wordLength-all.bin",from_file=True)

	for length in [2,3,4,5,6,7]:
		#print("Length =",length)
		matchCnt = 0
		for i in range(0,numWords):
			word = ''.join(model.generate(length=length, forced=True))
			#print(word)
			if word in t2w.words:
				matchCnt += 1
		#print(matchCnt)
		print('{:.4f}'.format(matchCnt/numWords),end="\t")
	print("")
	del model

print("\n-----------------------------------------------------------------------------\n")

###############################################################################################

print("Statistics for models trained with words of specific lengths.")
print("One model for each order and word length combination.\n")
print("\tWord Length")
print("Order\t2\t3\t4\t5\t6\t7")
for order in [1,2,3]:
	print(order,end="\t")

	for length in [2,3,4,5,6,7]:
		#print("Length =",length)

		words_as_lists_selected = [w for w in words_as_lists if len(w)==length]
		#print("Total number of words of length",wordlen,"=",len(words_as_lists_selected))

		#Fit model to input data and write to file.
		model = MarkovModel()
		model.fit(state_sequences=words_as_lists_selected, states=states, order=order)
		#model.tofile(filename="WebOfScience_abstracts_order-"+str(order)+"_wordLength-all.bin")

		#Load model from file. Do not write to file.
		#model.fit(filename="data_wiki_earth_order-1_wordLength-all.bin",from_file=True)

		matchCnt = 0
		for i in range(0,numWords):
			word = ''.join(model.generate(length=length, forced=True))
			#print(word)
			if word in t2w.words:
				matchCnt += 1
		#print(matchCnt)
		print('{:.4f}'.format(matchCnt/numWords),end="\t")
		del model
	print("")
print("")

###############################################################################################


print("Calculate probability of generation of a given word.\n")

model = MarkovModel()
model.fit(state_sequences=words_as_lists, states=states, order=2, replacenan=True)
print("Probability of word generation\n")
for word in ["earth","gravity","the","of","harsh","physics","encyclopedia","Blue","Marble","first","full","view","photograph","of","the","planet","was","taken","by","Apollo","astronauts","en","route","to","the","Moon","banana","bananax","sumedha"]:
	print("P(" + word + ") = " + '{:.16f}'.format(model.probability(word, verbose=True)) + "\n")


#Delete objects
del t2w
del words_as_lists


###############################################################################################
"""
sentences = [["Hello","world"], ["good","morning"], ["good","evening"], ["good","afternoon"], ["good","day"], ["i","eat","breakfast","in","morning"], ["i","do","exercise","in","evening"], ["in","evening","i","do","exercise"], ["he","is","having","breakfast"], ["earth","is","round"], ["earth","revolves","around","sun"], ["moon","revolves","around","earth"], ["sattelites","revolve","around","earth","as","well","as","around","moon","and","planets"], ["sattelites","revolve","around","moon"], ["satellites","revolve","around","planets"], ["mars","is","planet"], ["jupiter","is","planet"], ["sun","is","not","planet"], ["saturn","is","planet"]]

states = {}
for s in sentences:
	for w in s:
		if w not in states:
			states[w] = 0
		states[w] += 1

print(states)

print("Trying markov model for sentences.\n")

model = MarkovModel()
model.fit(state_sequences=sentences, states=["^"]+list(states.keys()), order=1, replacenan=True)

for i in range(0,50):
	sentence = ' '.join(model.generate(length=4, forced=True))
	print(sentence)

"""

