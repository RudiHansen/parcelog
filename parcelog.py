#!/usr/bin/python
# coding=utf-8

# Søger igennem alle logfiler fra /var/log/apache2 mappen og laver en liste
# over hvilke filer fra /upload mappen er blevet downloaded.
#
# Data gemmes i følgende felter, og skrives til en csv fil.
# Date	
# Time	
# Time zone	
# Country	
# WhoIS	
# IP Address
# File

from ipwhois import IPWhois
import gzip
import glob
import pprint
import time

runlogfilename	 = '/home/rsh/python/parcelog/runlog.log'
filepath         = '/var/log/apache2/'
filesearchpath   = '/var/log/apache2/access*'
filelastdatetime = 'lastdatetime.ini'
dictSaveWhoIs    = {}
lastDate         = ''
lastTime         = ''

# Function definition is here
def getIp( line ):
    pos1 = 0
    pos2 = line.find("-") - 1
    retStr = line[pos1:pos2]
    return retStr
    
def getTimeStamp( line ):
    pos1 = line.find("[") + 1
    pos2 = line.find("]")
    retStr = line[pos1:pos2]
    return retStr

def getDate( line ):
    pos1 = line.find("[") + 1
    pos2 = line.find(":",pos1)
    retStr = line[pos1:pos2]
    retStr = retStr.replace('Jan','01')
    retStr = retStr.replace('Feb','02')
    retStr = retStr.replace('Mar','03')
    retStr = retStr.replace('Apr','04')
    retStr = retStr.replace('May','05')
    retStr = retStr.replace('Jun','06')
    retStr = retStr.replace('Jul','07')
    retStr = retStr.replace('Aug','08')
    retStr = retStr.replace('Sep','09')
    retStr = retStr.replace('Okt','10')
    retStr = retStr.replace('Oct','10')
    retStr = retStr.replace('Nov','11')
    retStr = retStr.replace('Dec','12')

    day    = retStr[0:2]
    month  = retStr[3:5]
    year   = retStr[6:10]
    retStr = year + "/" + month + "/" + day
    return retStr

def getTime( line ):
    pos1 = line.find(":") + 1
    pos2 = pos1 + 8
    retStr = line[pos1:pos2]
    return retStr

def getTimeZone( line ):
    pos1 = line.find("+")
    pos2 = pos1 + 5
    retStr = line[pos1:pos2]
    return retStr

def getFileName( line ):
    pos1 = line.find("GET") + 4
    pos2 = line.find("HTTP")
    retStr = line[pos1:pos2]
    return retStr

def getWhoIs(ipadress):
    #return "BLA"
    if dictSaveWhoIs.has_key(ipadress):
	print "getWhoIs cache"
	return dictSaveWhoIs[ipadress]
    else:
	obj = IPWhois(ipadress)
	results = obj.lookup()
	nets = results['nets']
	if len(nets) > 0:
	    nets = nets[0]
	    retStr = results['asn_country_code'] + ";" + nets['description']
	    retStr = retStr.replace('\n', '')
	else:
	    retStr = ";"

    print "getWhoIs lookup"
    dictSaveWhoIs[ipadress] = retStr
    return retStr

def getFileList(filepath):
    filelist = glob.glob(filepath)
    filelist.sort()
    return filelist

def readFile(filename):
    inputfile = open(filename)

    for line in inputfile:
	if line.find("GET") > 0:
	    fileName = getFileName(line)
	    if fileName.find("uploads") > 0:
		dataLines.append(line)

    inputfile.close()
    return dataLines

def readFileGz(filename):
    inputfile=gzip.open(filename,'rb')

    for line in inputfile:
	if line.find("GET") > 0:
	    fileName = getFileName(line)
	    if fileName.find("uploads") > 0:
		dataLines.append(line)

    inputfile.close()
    return dataLines

def dataLines2DataRecordLines(dataLines = []):
    dataRecordLine = []

    for line in dataLines:
	ipadress 	= getIp(line)
	if ipadress == "80.71.134.194":
	    continue
	date		= getDate(line)
	time		= getTime(line)
	timeZone	= getTimeZone(line)
	fileName	= getFileName(line)
	if fileName.find("uploads") > 0:
	    dataRecord = []
	    whoIs = getWhoIs(ipadress)
	    dataRecord.append(date)
	    dataRecord.append(time)
	    dataRecord.append(timeZone)
	    dataRecord.append(whoIs)
	    dataRecord.append(ipadress)
	    dataRecord.append(fileName)
	    dataRecordLine.append(dataRecord)

    return dataRecordLine

def saveDataRecordLine(dataRecordLines = []):
    global lastDate
    global lastTime
    cnt = 0
    outputfile = open('access.log.record.csv', 'w')

    for dataRecord in dataRecordLines:
	outputfile.write(dataRecord[0] + ";" + dataRecord[1] + ";" + dataRecord[2] + ";" + dataRecord[3] + ";" + dataRecord[4] + ";" + dataRecord[5] + "\n")
	lastDate = dataRecord[0]
	lastTime = dataRecord[1]
	cnt += 1

    outputfile.close()
    print("Found {0} lines.".format(cnt))

def saveLastDateTime():
    global lastDate
    global lastTime
    outputfile = open(filelastdatetime, 'w')
    outputfile.write(lastDate+'\n')
    outputfile.write(lastTime+'\n')
    outputfile.close()

def nprint(header,data):
    print ">----" + header
    pprint.pprint(data)
    print len(data)
    print ">----" + header
    raw_input("Press Enter to continue...")

def writelog(logmessage):
    outputfile = open(runlogfilename,'a')
    outputfile.write('{0} : {1}\n'.format(time.strftime("%d/%m/%Y %H:%M:%S"),logmessage))

# Main code
writelog("Start parcelog.py")
filenames = getFileList(filesearchpath)
dataLinesSum = []

for filename in filenames:
	print filename
	dataLines = []
	if filename.find(".gz") > 0:
		dataLines = readFileGz(filename)
	else:
		dataLines = readFile(filename)
	
	dataLinesSum += dataLines

print "dataLines2DataRecordLines"
dataRecordLines = dataLines2DataRecordLines(dataLinesSum)
print "Sort list"
dataRecordLines.sort()
print "saveDataRecordLine"
saveDataRecordLine(dataRecordLines)
saveLastDateTime()
print lastDate + '-' + lastTime
writelog("End   parcelog.py")
