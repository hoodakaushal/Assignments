import sys
import os
import pdb

if not(os.path.isfile(sys.argv[1]) and  os.path.isfile(sys.argv[2])):
	print "Error:n Atleast one of file does not exist"
	sys.exit(1)

in_file_user = open(sys.argv[1],"r")
in_file_gold = open(sys.argv[2],"r")

lines_user = in_file_user.readlines()
lines_gold = in_file_gold.readlines()

num_lines_user=len(lines_user)
num_lines_gold=len(lines_gold)
in_file_user.close()
in_file_gold.close()
fpD=0.0
tpD=0.0
tnD=0.0
fnD=0.0
tpT=0.0
fpT=0.0
fnT=0.0
tnT=0.0
for i in range(num_lines_user):
	s_user=lines_user[i].split()
	s_gold=lines_gold[i].split()
	if(len(s_user)<=1):
		continue
	if(s_gold[1]==s_user[1]):
		if(s_gold[1]=="D"):
			print"hi"
			tpD=tpD+1
			tnT=tnT+1
		elif (s_gold[1]=="T"):
			tpT=tpT+1
			tnD=tnD+1
		else:
			tnD=tnD+1
			tnT=tnT+1
	else:
		if((s_user[1]=="D") and (s_gold[1]=="T")):
			fpD=fpD+1
			fnT=fnT+1
		elif((s_user[1]=="D") and (s_gold[1]=="O")):
			fpD=fpD+1
		elif((s_user[1]=="T") and (s_gold[1]=="D")):
			fpT=fpT+1
			fnD=fnD+1
		elif((s_user[1]=="T") and (s_gold[1]=="O")):
			fpT=fpT+1
		elif((s_user[1]=="O") and (s_gold[1]=="D")):
			fnD=fnD+1
			tnT=tnT+1
		else:
			fnT=fnT+1
			tnD=tnD+1
if((tpD==0)and(tpT==0)):
	microPrecision=0
	microRecall=0
else:
	microPrecision=((tpD+tpT)/(tpD+tpT+fpD+fpT))
	microRecall=(tpD+tpT)/(tpD+tpT+fnD+fnT)
if(tpD==0):
	p1=0
	r1=0
else:
	p1=tpD/(tpD+fpD)
	r1=tpD/(tpD+fnD)


if(tpT==0):
	p2=0
	r2=0
else:
	p2=tpT/(tpT+fpT)
	r2=tpT/(tpT+fnT)
macroPrecision=(p1+p2)/2
macroRecall=(r1+r2)/2
if((microPrecision==0)and(microRecall==0)):
	microF_Score=0
else:	
	microF_Score=2*microPrecision*microRecall/(microPrecision+microRecall)
if((macroPrecision==0)and(macroRecall==0)):
	macroF_Score=0
else:
	macroF_Score=2*macroPrecision*macroRecall/(macroPrecision+macroRecall)
print "microF_Score is tpT%f, " %(microF_Score) 
print "microPrecision is %f" %(microPrecision) 
print "microRecall is %f" %(microRecall)
print "macroF_Score is %f, " %(macroF_Score) 
print "macroPrecision is %f" %(macroPrecision) 
print "macroRecall is %f" %(macroRecall)


