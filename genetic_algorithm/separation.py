import os
import random
 
'''
This program takes in a aptamer and outputs an a apter with a dictionary of aptemers with 1 mutation
Input: aptamer string
Output: dictionary of aptamers with either 1 substitution or 1 addition
''' 
 
#function to replace a random site
 
#returns sequence with random site substituted (string) 
def sep (input_sequence):
	dictionary=[]
	s=list(input_sequence)
	for num in range(0, len(s)):
		templist=list(input_sequence)
		if templist[num]== 'A': 
			templist[num]='T'
			temp="".join(templist)
			dictionary.append(temp)
			
			templist[num]='G'
			temp="".join(templist)
			dictionary.append(temp)
		
			templist[num] ='C'
			temp="".join(templist)
			dictionary.append(temp)
		
		elif templist[num]== 'C':
			templist[num]='T'
			temp="".join(templist)
			dictionary.append(temp)
			
			templist[num]='G'
			temp="".join(templist)
			dictionary.append(temp)
		
			templist[num] = 'A' 
			temp="".join(templist)
			dictionary.append(temp)
			
		elif templist[num]== 'G':
			templist[num]='T'
			temp="".join(templist)
			dictionary.append(temp)
			
			templist[num]='C'
			temp="".join(templist)
			dictionary.append(temp)
			
			templist[num] = 'A'
			temp="".join(templist)
			dictionary.append(temp)
		
		elif templist[num]== 'T':
			templist[num]=='C'
			temp="".join(templist)
			dictionary.append(temp)
			
			templist[num]='G'
			temp="".join(templist)
			dictionary.append(temp)
		
			templist[num] == 'A'
			temp="".join(templist)
			dictionary.append(temp)
	for ins in range(0, len(s)+1):
		templist=list(input_sequence)
		templist.insert(ins, 'A')
		temp="".join(templist)
		dictionary.append(temp) 
		
		templist=list(input_sequence)
		templist.insert(ins, 'C')
		temp="".join(templist)
		dictionary.append(temp)
		
		templist=list(input_sequence)
		templist.insert(ins, 'G')
		temp="".join(templist)
		dictionary.append(temp)
		
		templist=list(input_sequence)
		templist.insert(ins, 'T')
		temp="".join(templist)
		dictionary.append(temp)
	for delet in range (0, len(s)):
		templist=list(input_sequence)
		templist[delet]=''
		temp="".join(templist)
		dictionary.append(temp)
		
	return dictionary

 
aptemer ="AACCGGTT"
newA =sep(aptemer)
#print (newA)
#print("hello world")
