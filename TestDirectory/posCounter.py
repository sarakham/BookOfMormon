from bomArffGenerator import *
from random import *

############################################################
# DESCRIPTION:
#
# This script creates a data structure called "data" which 
# counts each part of speech (referred to here as "pos") and
# adds the count and enumeration of the individual parts of speech
# to the structure called "data."  An example is seen just below.  
############################################################

import os

############################################################
# Example of the final data structure:
# { 'Nephi': 
#			[
#				#block 0
#				{'NN': [10, ['nephi', 'bob', 'noun'...]],
#				 'AJ': [20, ['quikly', 'sharply', 'adjictive'...]],
#				 ...,
#				"Interjections":{'yea': 3, 'behold': 1, 'wo': 1} 
#				},
#				 #block 1 
#				 {'NN': [1,['obo']], ...,"Interjections":{'yea': 3, 'behold': 1, 'wo': 1}},
#				 #block n
#				 ...
#			]
#	'Alma': [...],
#	...
# }
############################################################
data = {}


############################################################
# This function will process a file that represents the number
# of interjections that a author used in a given block and adds
# it to 'data'
############################################################
def process_author_interjection_file(fileName):
        file = open(fileName, 'r')
        ret_dict = eval(file.read())
        file.close()
        return ret_dict


############################################################
# This function will open a file (an author's n^th block of text)
# and add it to the author's current list of blocks in "data."
# It will also add all of the parts of speech (pos) the author used
# in that block and count them as well
############################################################
def process_author_file(fileName):

	# author, end = fileName.split('-')
	# block, extension = end.split('.')

	author, txt_block, end = fileName.split('_')
	block, extension       = end.split('.')

	#print author, block

	inter_dict = process_author_interjection_file(author+'-'+block+'-interjections.inter')

	# Adds the author to "data" if they aren't already there
	if not author in data.keys():
		data[author] = []

	# Generate block from file
	block_file = open(fileName, 'r')
	block = {}
	for word_and_pos in block_file:
		word, pos = word_and_pos.strip().split('/')

		# Add the Part of Speech if not already seen
		if not pos in block.keys():
			block[pos] = []
			block[pos].append(0)
			block[pos].append([])

		block[pos][0] = block[pos][0] + 1 	#Count the number of Parts of Speech
		block[pos][1].append(word)			#Keep track of each Part of Speech

	# Include interjection dictionary in block
	block['Interjections'] = inter_dict
        
	# Add block to author
	data[author].append(block)

	return

def remove_authors_with_small_numbers_of_blocks():
	threshold = 69
	keys = data.keys()
	count = 0
	for key in keys:
		if len(data[key]) <= threshold:
			del data[key]
			count = count + 1

	print 'Removed \'', count, '\' authors from data due to block count less than \'', threshold,'\''
	print 'Keeping', len(data), 'authors.'


def undersample_with_num_blocks(num_blocks, data):

	for author in data.keys():
		num_blocks = len(data[author])

		#Generate array of random indexes to pull out...
		sample_indexes = []
		for i in range(0, 70):
			rand_index = randint(0,num_blocks-1)
			while rand_index in sample_indexes:
				rand_index = randint(0,num_blocks-1)

			sample_indexes.append(rand_index)

		undersampled_data = []
		for i in sample_indexes:
			undersampled_data.append(data[author][i])

		print len(data[author]), len(undersampled_data)
		data[author] = undersampled_data

	return
    
# # Prepares the data for binary comparison (i.e., one author vs the rest)
# def prepare_for_binary_comparison(author_name):
#     
#     
#     return
    
# Prints the number of blocks each author has
def print_numbers_of_blocks_per_author():
    
    print "\n"
    for author in data.keys():
        print author, len(data[author]), "blocks"
    print"\n"        
    return

############################################################
# Goal: Nice Data structure to query any pos statistic 
#		required.
############################################################
if __name__ == '__main__':
	cnt = 0

	for fileName in os.listdir("."):
	    if fileName.endswith(".txt"):
	    	cnt = cnt + 1
	    	process_author_file(fileName)

	print ("Processed: ", cnt, " \".txt\" files.")

	#Clean Authors: Remove Authors with less than 10 Blocks
	remove_authors_with_small_numbers_of_blocks()
    
	#UnderSample
# 	undersample_with_num_blocks(70, data)
    
        print_numbers_of_blocks_per_author()
        prepare_for_binary_comparison("NEPHI (SON OF LEHI)")

	print ("Data structure written to data.data for review.")
	data_file = open('../data.data', 'w')
	data_file.write(str(data))

	write_data_to_weka_data_file(data, '../test.arff')

	print ("...Done.")

