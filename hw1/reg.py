import re

mystr = 'This is a st_ring, wit2h wo-rd\'s!'
wordList = re.sub("[^\w]", " ",  mystr).split()
otherWordList = re.sub('[^a-z\ \-\']+', " ", mystr.lower()).split()

book = {'str' : [0,1,2], 'int' : [10,20,30]}
book['str'][0] = 100
print(book)
print(wordList)
print(otherWordList)