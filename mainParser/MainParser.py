import glob
import re

fileList = []
commentPatterns = [re.compile("\/\/.*"), re.compile("\/\*.*\*\/")]


fileList = glob.glob("*")

for file_index in range(len(a)-1):
	with open(a[file_index]) as f:
    	content = f.readlines()

for row_index in range(len(content)-1):
	for pattern_index in range(len(commentPatterns)):
		if content[row_index].match(commentPatterns[pattern_index]):
			 