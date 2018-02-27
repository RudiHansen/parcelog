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
import time

runlogfilename	= '/home/rsh/python/parcelog/runlog.log'
filenamecsv	= '/home/rsh/python/parcelog/access.log.record.csv'
filenamehttp	= '/var/www/info/downloadfilelog.html'

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

def writelog(logmessage):
    outputfile = open(runlogfilename,'a')
    outputfile.write('{0} : {1}\n'.format(time.strftime("%d/%m/%Y %H:%M:%S"),logmessage))

def pause():
    raw_input("Press Enter to continue...")

# Main code
writelog("Start csv2http.py")
dataLines = readFile(filenamecsv)
dataLines.sort(reverse=True)
writeFile(filenamehttp,dataLines)
writelog("End   csv2http.py")
