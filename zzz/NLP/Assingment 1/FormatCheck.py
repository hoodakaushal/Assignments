import sys
import os
import pdb


num_tweets = 1272
if not(os.path.isfile(sys.argv[1])):
	print "Error: File does not exist"
	sys.exit(1)

in_file = open(sys.argv[1],"r")
lines = in_file.readlines()
num_lines = len(lines)
in_file.close()

line = 0
for i in range(num_tweets):
	if line>=num_lines:
		print "Error: Tweet %d is missing" %(i+1)
		sys.exit(1)
	tweet = lines[line].strip()
	line += 1
	
	try:
		if line>=num_lines:
			print "Error: Number of tokens for tweet %d is missing" %(i+1)
			sys.exit(1)
		num_tokens = int(lines[line])
	except ValueError:
		print "Error: Line %d is not integer (number of tokens)" %(line+1)
		sys.exit(1)
	line += 1

	if line+num_tokens-1>=num_lines:
		print "Error: Expected more tokens in tweet %d" %(i+1)
		sys.exit(1)

	line += num_tokens

if line != num_lines:
	print "Error: Expected less lines in the file"
	sys.exit(1)


num_tweets = 29
