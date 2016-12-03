#!/usr/bin/python
#
# scorer for NLP class Spring 2016
# ver.1.0
#
# score a key file against a response file
# both should consist of lines of the form:   token \t tag
# sentences are separated by empty lines
#
import sys
import re
import os
import random

def score (keyFileName, responseFileName,total_queries=225,total_documents=1400,trace=False):
	## assumes that Cranfield Corpus is the default
	keyFile = open(keyFileName, 'r')
	key = keyFile.readlines()
	key_dict = {}
	responseFile = open(responseFileName, 'r')
	response = responseFile.readlines()
	response_dict = {}
	all_precisions = []
	all_recalls = []
	missing_responses = []
	for line in key:
		line = line.rstrip(os.linesep)
		line = line.rstrip(' ')
		query,abstract,score = re.split(' +',line)
		query = int(query)
		abstract = int(abstract)
		score = int(score)
		if abstract <= total_documents:
			## gets rid of some of the "extra" documents
			## there seem to be some abstracts mentioned in the
			## answer key that don't exist (those above 1400)
			## we will ignore these
			if query in key_dict:
				if not abstract in key_dict[query]:
					key_dict[query].append(abstract)
			else:
				key_dict[query] = [abstract]
	for line in response:
		line = line.rstrip(os.linesep)
		line = line.rstrip(' ')
		query,abstract,score = re.split(' +',line)
		if not (query.isdigit() and abstract.isdigit() and re.search('^[0-9\.-]+$',score)):
			print('Warning: Each line should consist of 3 numbers with a space in between')
			print('This line does not seem to comply:',line)
			exit()
		query = int(query)
		abstract = int(abstract)
		score = float(score)
		if query in response_dict:
			if not abstract in response_dict[query]:
				response_dict[query].append(abstract)
				## these are listed in order, based on score
		else:
			response_dict[query] = [abstract]
	for query_id in key_dict: 
		## for query_id in range(1,total_queries):
		if (query_id in key_dict):
			total_answers =	len(key_dict[query_id])
		else:
			total_answers = 0
		if (query_id in key_dict) and (query_id in response_dict):
			correct = 0
			incorrect = 0
			so_far = 0
			milestone = .1
			precisions = []
			recordable_recall = 0
			for abstract_id in response_dict[query_id]:
				so_far = so_far+1
				if abstract_id in key_dict[query_id]:					
					correct = correct + 1
					recall = float(correct)/float(total_answers)
					if (correct+incorrect)<=total_answers:
						recordable_recall = recall
					while recall>milestone:
						precisions.append(float(correct)/float(correct+incorrect))
						milestone = milestone+.1
				else:					
					incorrect = incorrect+1
			if len(precisions)>0:
				average_precision = (sum(precisions))/len(precisions)
			else:
				missing_responses.append(query_id)
			if trace:
				print(query_id,average_precision)
			all_precisions.append(average_precision)
			all_recalls.append(recordable_recall)
		elif query_id in key_dict:
			all_recalls.append(0)
	print 'Queries with No responses:'+str(missing_responses)
	MAP = sum(all_precisions)/len(all_precisions)
	Recall = sum(all_recalls)/len(all_recalls)
	print 'Average MAP is: '+str(MAP)
	print 'Average Recall is: '+str(Recall)

def get_triple_from_line(line):
	line = line.rstrip(os.linesep)
	line = line.rstrip(' ')
	query,abstract,score = re.split(' +',line)
	query = int(query)
	abstract = int(abstract)
	score = float(score)
	return(query,abstract,score)

def print_remaining_triples(last_query,abstracts,outstream,total_responses):
	items = list(range(1,total_responses+1))
	random.shuffle(items)
	for item in items:
		if not item in abstracts:
			outstream.write(str(last_query)+' '+str(item)+' 4'+os.linesep)
	

def make_random_response(infile,outfile,total_responses=1400):
	middle_number = re.compile(' ([0-9]+) ')
	last_query = 0
	abstracts = []
	with open(infile) as instream:
		with open(outfile,'w') as outstream:
			for line in instream.readlines():
				query,abstract,score = get_triple_from_line(line)
				if abstract > total_responses:
					## ignore "extra" abstracts
					pass
				elif (last_query!=0) and (query!=last_query):
					print_remaining_triples(last_query,abstracts,outstream,total_responses=1400)
					abstracts =[]
				last_query = query
				choice = random.random()
				if abstract > total_responses:
					## ignore "extra" abstracts"
					pass
				elif choice < .25:
					pass
				elif choice < .75:
					if not abstract in abstracts:
						outstream.write(line)
						abstracts.append(abstract)
				else:
					match = middle_number.search(line)
					if match:
						new_numbers = []
						for number in range(random.randint(1,4)):				
							number = int(match.group(1))+random.randint(1,100)
							newline = line[:match.start(1)]+str(number)+line[match.end(1):]
							if (not number in abstracts) and (not number> total_responses):
								outstream.write(newline)
								abstracts.append(number)
			print_remaining_triples(last_query,abstracts,outstream,total_responses)

def main(args):
	key_file = args[1]
	response_file = args[2]
	if (len(args)>3) and (args[3].lower() in ['true','t']):
		score(key_file,response_file,trace=True)
	else:
		score(key_file,response_file)

if __name__ == '__main__': sys.exit(main(sys.argv))
