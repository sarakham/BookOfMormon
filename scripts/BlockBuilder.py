# Wes

import os
import re

# Returns an array with all the words from the file in it
#    file - handle to the open file to be read
#    blocks_directory - author-specific directory to write the blocks of text
#    filename - the name of the file (when written, the block number is appended)
def getBlocks(file, blocks_directory, filename):
    # create ouput directory for the blocks for each author
    print "==========\n BLOCKS FOR:", filename, "\n=========="
    if not os.path.exists(blocks_directory):
        os.makedirs(blocks_directory)
     
    # remove newlines and hyphens, put in array
    text = file.read()
    text = text.strip('\n').replace('--', ' ').replace('\n', ' ')
    text = re.sub(' +', ' ', text)
    text_array = text.split(' ')
     
    # count words 
    length =  len(text_array)
    numBlocks = length/200
    print "Numblocks", numBlocks
 
    # create blocks of 200 words and write to file       
    curblock = ""
    offset = 0;
    for block in range(0, numBlocks):
        print "----\nBlock:", block, "\n----"
        # get 200 words for the block
        for word in range((0+offset), (200+offset)):
            curblock = curblock + " " + text_array[word]
        
        # write block to a file in author-specific folder (blocks_directory)
        file_directory = blocks_directory + "/" + filename + "_block_" + str(block) + ".txt"
        block_file = open(file_directory, 'w+')
        block_file.write(curblock)
        block_file.close()
        
        # update offset and curblock 
        offset = offset + 200
        print curblock
        print "\t Written to:", file_directory
        curblock = ""
    
    
""" load the files """
INPUT_PATH = "/home/wes/Documents/bom/bom/200WordAuthors/"
OUTPUT_PATH = "/home/wes/Documents/bom/bom/200WordBlocks/"
dir_contents = os.listdir(INPUT_PATH)   # this folder CANNOT HAVE SUB-FOLDERS or .read() will break
 
# Break each author's text into blocks of 200 words
for x in range(0, len(dir_contents)):
    #open the file
    file = dir_contents[x] 
    file_path = INPUT_PATH + file
    output_file = OUTPUT_PATH + file
     
#     print "output", output_file
    file = open(file_path, 'r')
    
    block_output_path = OUTPUT_PATH + dir_contents[x].strip('.txt')
    temp = getBlocks(file, block_output_path, dir_contents[x].strip('.txt.'))

print "\n\nDone!"     
