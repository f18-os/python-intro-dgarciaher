import string

# Creates dictionary to keep track of words as they appear
wordCount = {}

# Takes name of the output file
outName = input('Enter output file name: ')
outFile = open(outName, "w")
# Takes name of the input file
inName = input('Enter input file name: ')
inFile = open(inName, "r")

# removes special characters that might interfere with the word being recognized
for word in inFile.read().split():
    isolatedWord = ""
    for specialChar in word:
        if specialChar not in string.punctuation:
            isolatedWord += specialChar

    # Adds word to the dictionary
    if isolatedWord.lower() not in wordCount:
        wordCount[isolatedWord.lower()] = 1
    # Increases the count for the word if it has already been identified
    else:
        wordCount[isolatedWord.lower()] += 1

# Writes to output file each word and how many times it appeared from the dictionary
for a, b in wordCount.items():
    outFile.write(str(a) + '-> appears: ' + str(b) + ' times' + '\n\n')

outFile.close()
