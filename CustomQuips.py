# Creates custom Quiplash 2 Questions
# Used instead of in-game question creator so you can use commands 
# like <ANY PLAYER> to select a random player name and <BLANK> to create blank space within questions

# Reads questions from file
# Creates QuiplashQuestion.jet (QL file for all questions)
# Creates tts for questions (in .ogg format) - potentially implement FakeYou deepfake tts
# Creates individual folders for each question with the audio file and data.jet

# QuiplashQuestions.jet example - '{"content":[{"x":false,"id":35008,"prompt":"The gross thing nobody knows about the Easter Bunny"}],"episodeid":1251}'
# \u2019 = apostrophe, \u201c = opening speech mark, \u201d = closing speech mark

import os, re


### Creating new directory

# for item in os.listdir('./'):
# 	if os.path.isdir(os.path.join('./', item)):
# 		print(item)
dirs = [item for item in os.listdir('./') if os.path.isdir(os.path.join('./', item))] # List comprehension to create list of directories in rootdir
cqldirs = [int(x.split('CQL ')[1]) for x in dirs if re.match(r'CQL .*',x)] # list of dirs starting with "CQL"
cqldirs.append(0) # Adds 0, so list isnt empty
newdir = 'CQL '+str(max(cqldirs)+1)
os.mkdir(newdir)

# ### Creating QuiplashQuestions.jet

def createid(n): # Creates an ID using the questions index, turning it into a 5 digit number
	digits = len(str(len(cqlist)))
	if digits < 5:
		return ('00000'+str(n))[-5:]
	else:
		return ('0'*digits+str(n))[-5:]


customqs = open('customquestions.txt','r')
cqlist = customqs.read().split('\n') # List of all custom questions
customqs.close()

qqjet = '{"content":['
n = 1

for x in cqlist:
	question = x.replace("'","\\u2019")
	idnumber = '0'*2*len(str(len(cqlist)))+str(n)
	qqitem = '{"x":false,"id":'+createid(n)+',"prompt":"'+question+'"},'
	qqjet = qqjet + qqitem
	n+=1

qqjet = qqjet[:-1] + '],"episodeid":1251}' # removes last comma in string and completes text

qqjetfile = open(f'./{newdir}/QuiplashQuestions.jet','w')
qqjetfile.write(qqjet)
qqjetfile.close()

