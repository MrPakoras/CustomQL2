# Creates custom Quiplash 2 Questions
# Used instead of in-game question creator so you can use commands 
# like <ANY PLAYER> to select a random player name and <BLANK> to create blank space within questions

# Reads questions from file
# Creates QuiplashQuestion.jet (QL file for all questions)
# Creates tts for questions (in .ogg format) - potentially implement FakeYou deepfake tts
# Creates individual folders for each question with the audio file and data.jet

# QuiplashQuestion.jet example - '{"content":[{"x":false,"id":35008,"prompt":"The gross thing nobody knows about the Easter Bunny"}],"episodeid":1251}'
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
os.mkdir(newdir) # make newdir

# ### Creating QuiplashQuestion.jet

def createid(n): # Creates an ID using the questions index, turning it into a 5 digit number
	digits = len(str(len(cqlist)))
	if digits < 5:
		return ('00000'+str(n))[-5:]
	else:
		return ('0'*digits+str(n))[-5:]

def filewrite(dir,text):
	f = open(dir,'w')
	f.write(text)
	f.close()


customqs = open('customquestions.txt','r')
cqlist = customqs.read().split('\n') # List of all custom questions
customqs.close()

qqjet = '{"content":['
n = 1

for x in cqlist:
	question = x.replace("'","\\u2019") # Replaces apostrophes in question to be readable by game code
	idnumber = '0'*2*len(str(len(cqlist)))+str(n) # Question ID
	audioid = idnumber+'_0' # ID for question audio file
	questiondir = f'{newdir}/{idnumber}' # subdir for each question
	os.mkdir(questiondir)
	questiondata = '{"fields":[{"t":"B","v":"false","n":"HasJokeAudio"},{"t":"S","v":"","n":"Keywords"},{"t":"S","v":"","n":"Author"},{"t":"S","v":"","n":"KeywordResponseText"},{"t":"S","v":"'+question+'","n":"PromptText"},{"t":"S","v":"","n":"Location"},{"t":"A","n":"KeywordResponseAudio"},{"t":"A","v":"'+audioid+'","n":"PromptAudio"}]}'
	filewrite(f'{questiondir}/data.jet',questiondata) # Writes questiondata to data.jet in question subdir
	qqitem = '{"x":false,"id":'+createid(n)+',"prompt":"'+question+'"},' # Each question item for QuiplashQuestion.jet
	qqjet = qqjet + qqitem
	n+=1

qqjet = qqjet[:-1] + '],"episodeid":1251}' # removes last comma in string and completes text

filewrite(f'./{newdir}/QuiplashQuestion.jet',qqjet) # Write qqjet to file




# qqjetfile = open(f'./{newdir}/QuiplashQuestion.jet','w')
# qqjetfile.write(qqjet)
# qqjetfile.close()

