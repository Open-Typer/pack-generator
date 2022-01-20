#!/usr/bin/python3

# create-wordlist.py
# This file is part of Open-Typer
#
# Copyright (C) 2022 - adazem009
#
# Open-Typer is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Open-Typer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Open-Typer. If not, see <http://www.gnu.org/licenses/>.

import sys
import string

def printUsage():
	print("Usage:\n"+sys.argv[0]+" <input files> -o outputFile")

def processFile(fileName):
	charExceptions = "'‘"
	silentCharExceptions = "-"
	inputFile = open(fileName,"r")
	# Create word list
	lines = inputFile.read().splitlines()
	wordlist = list()
	for line in lines:
		words = line.split()
		for word in words:
			newWord = ''
			for ch in word:
				charException = False
				if(ch in charExceptions):
					print("Allow character '" + ch + "' in word \"" + word + "\"? (Y/N)")
					answer = input()
					if answer == "y" or answer == "Y":
						charException = True
				if(ch in silentCharExceptions):
					charException = True
				if not ch in string.punctuation and ch.isalpha() or charException:
					newWord += ch
			if len(newWord) >= 3 and not newWord in wordlist:
				wordlist.append(newWord)
	inputFile.close()
	# Generate output string
	out = ''
	for word in wordlist:
		out += word + '\n'
	return out

# Read args
inputFiles = list()
outname = ""
i = 1
while i < len(sys.argv):
	if sys.argv[i][0] == '-':
		if sys.argv[i] == "-o":
			i += 1
			if i == len(sys.argv):
				print(sys.argv[0]+": missing file operand")
				exit(3)
			outname = sys.argv[i]
		else:
			printUsage()
			exit(1)
	else:
		inputFiles.append(sys.argv[i])
	i += 1
if len(inputFiles) == 0 or outname == "":
	printUsage()
	exit(4)

# Open input and output files
out = open(outname,"w")

# Process all input files
for fileName in inputFiles:
	out.write(processFile(fileName))
out.close()
