from TWordVec import WordVec
import numpy as np
import random
import pickle as pkl
import sys
WORD_DIM = 300
FILE_NAME = raw_input("enter filename : ")
model = WordVec()


def findMaxLenght():
	temp = 0
	max_lenght = 0

	for line in open(FILE_NAME):
		if line in ['\n', '\r\n']:
			if temp > max_lenght:
				max_lenght = temp
			temp = 0
		else:
			temp += 1

	return max_lenght 

def seed_unknown(st):
	assert(len(st) > 0)

	if len(st) == 1:
		return ord(st)
	else:
		ans = 1
		for i in range(len(st)):
			ans *= ord(st[i])
		return ans


def get_input():
	word = []
	tag = []

	sentence = []
	sentence_tag = []

	#get max words in sentence
	max_sentence_length = findMaxLenght()
	sentence_length = 0

	print "size is : " + str(max_sentence_length)


	for line in open(FILE_NAME):
		if line in ['\n', '\r\n']:
#	print "aa"	
			for _ in range(max_sentence_length - sentence_length):
				tag.append(np.array([0,0,0,0,0]))
				temp = [0 for _ in range(WORD_DIM)]
				word.append(temp)
				
			
#			assert (len(word) == 113)
#			assert (len(tag) == 113)

			sentence.append(word)
			sentence_tag.append(np.array(tag))

			sentence_length = 0	
			word = []
			tag = []


		else:
			assert(len(line.split()) == 4)
			sentence_length += 1

			try:
				word.append(model.genVec(line.split()[0]))
			except:
				random.seed(seed_unknown(line.split()[0]))
#				print "not in vocab"

				noob = [random.random() for _ in xrange(WORD_DIM)]
				word.append(noob)

			t = line.split()[3]

			# Five classes 0-None,1-Person,2-Location,3-Organisation,4-Misc

			if t.endswith('O'):
				tag.append(np.array([1, 0, 0, 0, 0]))
			elif t.endswith('PER'):
				tag.append(np.array([0, 1, 0, 0, 0]))
			elif t.endswith('LOC'):
				tag.append(np.array([0, 0, 1, 0, 0]))
			elif t.endswith('ORG'):
				tag.append(np.array([0, 0, 0, 1, 0]))
			elif t.endswith('MISC'):
				tag.append(np.array([0, 0, 0, 0, 1]))
			else:
				print t
				print "error in input"
				sys.exit(0)

	assert(len(sentence) == len(sentence_tag))
	print sentence_tag[0]
	pkl.dump(sentence,open('s','w'))
	pkl.dump(sentence_tag,open('s_tag','w'))

get_input()

