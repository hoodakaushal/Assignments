import sys
import os
import pdb

num_tweets = 3

if not(os.path.isfile(sys.argv[1]) and  os.path.isfile(sys.argv[2])):
	print "Error:n Atleast one of file does not exist"
	sys.exit(1)


in_file_user = open(sys.argv[1],"r")
in_file_gold = open(sys.argv[2],"r")
lines_user = in_file_user.readlines()
lines_gold = in_file_gold.readlines()

in_file_user.close()
in_file_gold.close()

line_user=0
line_gold=0
tp=0.0
fp=0
fn=0
for i in range(num_tweets):
	tp_tweet=0.0
	tweet_user=lines_user[line_user].strip()
	tweet_gold=lines_gold[line_gold].strip()
	line_user=line_user+1
	line_gold=line_gold+1
	ntokens_user=int(lines_user[line_user])
	ntokens_gold=int(lines_gold[line_gold])
	line_user=line_user+1
	line_gold=line_gold+1
	tweet_dict=dict()
	for j in range(ntokens_gold):
		key=lines_gold[line_gold].strip()
		line_gold=line_gold+1
		if key in tweet_dict.keys():
			tweet_dict[key]=tweet_dict[key]+1
		else:
			tweet_dict[key]=1
	for k in range(ntokens_user):
		key=lines_user[line_user].strip()
		line_user=line_user+1
		if key in tweet_dict.keys():
			tweet_dict[key]=tweet_dict[key]-1
			if(tweet_dict[key]==0):
				del tweet_dict[key]
			tp_tweet=tp_tweet+1
	fn=fn+ntokens_gold-tp_tweet
	fp=fp+ntokens_user-tp_tweet
	tp=tp+tp_tweet
precision=tp/(tp+fp)
recall=tp/(tp+fn)
f_score=2*precision*recall/(precision+recall)

print "F_Score is %f, " %(f_score) 
print "Precision is %f" %(precision) 
print "Recall is %f" %(recall)
				
		
			


