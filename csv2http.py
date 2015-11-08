#!/usr/bin/python
# coding=utf-8

# Convertere .csv fil med logdata til en html fil
# .csv filen indeholder følgende felter
# Date	
# Time	
# Time zone	
# Country	
# WhoIS	
# IP Address
# File

filenamecsv	= 'access.log.record.csv'
filenamehttp	= '/var/www/downloadfilelog.html'

# Function definition is here
def readFile(filenamecsv):
    dataLines	= []
    inputfile	= open(filenamecsv)

    for line in inputfile:
	line	= line.rstrip(' \n')
	fields	= line.split(';')
	dataLines.append(fields)

    inputfile.close()
    return dataLines

def writeFile(filenamehttp,dataLines):
    outputfile = open(filenamehttp,'w')
    outputfile.write('<table border="1" style="border:1px black;width:100%;border-collapse:collapse;">\n')
    for fields in dataLines:
	outputfile.write('<tr>\n')
	outputfile.write('<td>{0}</td>\n'.format(fields[0]))
	outputfile.write('<td>{0}</td>\n'.format(fields[1]))
	outputfile.write('<td>{0}</td>\n'.format(fields[2]))
	outputfile.write('<td>{0}</td>\n'.format(fields[3]))
	outputfile.write('<td>{0}</td>\n'.format(fields[4]))
	outputfile.write('<td>{0}</td>\n'.format(fields[5]))
	outputfile.write('<td>{0}</td>\n'.format(fields[6]))
	outputfile.write('</tr>\n')

    outputfile.write('</table>')
    outputfile.close()

def pause():
    raw_input("Press Enter to continue...")

# Main code
dataLines = readFile(filenamecsv)
dataLines.sort(reverse=True)
writeFile(filenamehttp,dataLines)