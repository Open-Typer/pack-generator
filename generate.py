#!/usr/bin/python3

# generate.py
# This file is part of Open-Typer
#
# Copyright (C) 2021-2022 - adazem009
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
import os
import random

def printUsage():
	print("Usage:\n"+sys.argv[0]+" inputFile -w wordlistFile -o outputFile")

def generate(usableCharacters, importantCharacters, sepCharacters, uppercaseKnown):
	if len(usableCharacters) == 0:
		return ""
	out = ""
	if len(usableCharacters) <= 2:
		for i in range(len(usableCharacters)):
			if not usableCharacters in sepCharacters:
				out += usableCharacters[i]*2
				if i+1 < len(usableCharacters):
					out += ' '
	else:
		words = random.randint(1,15)
		for i1 in range(words):
			for i2 in range(4):
				getid = random.randint(0,len(usableCharacters)-1)
				i3 = 0
				while (not usableCharacters[getid] in importantCharacters) and i3 < 5:
					getid = random.randint(0,len(usableCharacters)-1)
					i3 += 1
				while usableCharacters[getid] in sepCharacters:
					getid = random.randint(0,len(usableCharacters)-1)
				if i2 == 0 and uppercaseKnown and len(usableCharacters[getid].encode()) == 1:
					if random.randint(0,1) == 1:
						out += usableCharacters[getid].swapcase()
				else:
					out += usableCharacters[getid]
			if len(sepCharacters) > 0:
				out += sepCharacters[random.randint(0,len(sepCharacters)-1)]
			if i1+1 < words:
				out += ' '
	return out

def generateExercise(lesson, sublesson, exercise, lessonDesc, lessonCharacters, allCharacters, sepCharacters, uppercaseKnown, customText = ''):
	exerciseID = str(lesson) + '.' + str(sublesson) + '.' + str(exercise)
	if customText == '':
		exerciseID += ":1,w;120,60"
	else:
		exerciseID += ":0,0;120,60"
	if exercise == 1:
		exerciseID += ',' + lessonDesc
	exerciseID += ' '
	if customText == '':
		add = generate(allCharacters,lessonCharacters,sepCharacters,uppercaseKnown)
	else:
		add = customText
	if add == "":
		return add
	else:
		return exerciseID + add

# Read args
packname = ""
outname = ""
wordlist = ""
i = 1
while i < len(sys.argv):
	if sys.argv[i][0] == '-':
		if sys.argv[i] == "-o":
			i += 1
			if i == len(sys.argv):
				print(sys.argv[0]+": missing file operand")
				exit(3)
			outname = sys.argv[i]
		elif sys.argv[i] == "-w":
			i += 1
			if i == len(sys.argv):
				print(sys.argv[0]+": missing file operand")
				exit(3)
			wordlist = sys.argv[i]
		else:
			printUsage()
			exit(1)
	else:
		if packname == "":
			packname = sys.argv[i]
		else:
			printUsage()
			exit(2)
	i += 1
if packname == "" or outname == "":
	printUsage()
	exit(4)
# Open input and output files
config = open(packname,"r")
if wordlist == "":
	print(sys.argv[0]+": warning: no word list file specified")
	wordlistAvailable = False
else:
	if os.path.isfile(wordlist):
		wordlistFile = open(wordlist,"r")
		wordlistAvailable = True
	else:
		wordlistAvailable = False
out = open(outname,"w")
# Init variables
characters = ""
sepCharacters = ",;"
knownSepCharacters = ""
uppercaseKnown = False
lesson = 1
sublesson = 1
exercise = 1
random.seed(0)
# Generate lessons
for line in config:
	tmpline = line[:-1]
	line = ""
	lessonDesc = ""
	i = 0
	while i < len(tmpline):
		if tmpline[i] == ',' or tmpline[i] == ';' or tmpline[i] == '\\':
			if tmpline[i] == '\\':
				lessonDesc += tmpline[i] + tmpline[i+1]
				i += 1
			else:
				line += tmpline[i]
				lessonDesc += '\\' + tmpline[i]
		else:
			if tmpline[i] == '%':
				lessonDesc += tmpline[i] + tmpline[i+1]
				i += 1
				if tmpline[i] == 's':
					uppercaseKnown = True
				if tmpline[i] == '%':
					line += '%'
			else:
				line += tmpline[i]
				lessonDesc += tmpline[i]
		i += 1
	# One new character per exercise
	currentCharacters = ""
	for ch in line:
		if ch in sepCharacters:
			knownSepCharacters += ch
		currentCharacters += ch
		if ch != line[0]:
			add = generateExercise(lesson,sublesson,exercise,lessonDesc,line,currentCharacters,"",uppercaseKnown)
			if add != "":
				out.write(add + '\n')
				exercise += 1
	# Exercises with all known characters
	characters += line
	for i in range(5):
		add = generateExercise(lesson,sublesson,exercise,lessonDesc,line,characters,knownSepCharacters,uppercaseKnown)
		if add != "":
			out.write(add + '\n')
			exercise += 1
	# Word exercises (only works with a word list)
	if(wordlistAvailable):
		sublesson += 1
		exercise = 1
		availableWords = list()
		wordlistFile.seek(0)
		wordlistLines = wordlistFile.read().splitlines()
		for wordlistLine in wordlistLines:
			words = wordlistLine.split()
			for word in words:
				wordUsable = True
				for ch in word:
					if (not ch in characters and not ch.swapcase() in characters) or (ch.isupper() and not uppercaseKnown):
						wordUsable = False
						break
				if wordUsable:
					availableWords.append(word)
		if len(availableWords) >= 5:
			for i in range(5):
				text = ''
				for i2 in range(random.randint(10,50)):
					word = availableWords[random.randint(0,len(availableWords)-1)]
					sepChar = knownSepCharacters[random.randint(0,len(knownSepCharacters)-1)]
					if text == '':
						text = word + sepChar
					else:
						text += ' ' + word + sepChar
				add = generateExercise(lesson,sublesson,exercise,lessonDesc,None,None,None,None,text)
				if add != "":
					out.write(add + '\n')
					exercise += 1
	lesson += 1
	sublesson = 1
	exercise = 1
config.close()
if(wordlistAvailable):
	wordlistFile.close()
out.close()
