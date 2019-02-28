#!/usr/bin/python
import os
import sys
import ntpath
import time
import re
import urlparse, urllib2
import hashlib


class bcolors:
    TITLE = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    INFO = '\033[93m'
    OKRED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGRED = '\033[41m'
    UNDERLINE = '\033[4m'
    FGWHITE = '\033[37m'
    FAIL = '\033[95m'



rootDir=os.path.expanduser("~")+"/.SourceCodeAnalyzer/" #ConfigFolder ~/.SourceCodeAnalyzer/
projectDir=""
apkFilePath=""
apkFileName=""
firbaseProjectList=[]
inScoprUrls=[]
apkHash=""
apktoolPath="./Dependencies/apktool_2.3.4.jar"

def myPrint(text, type):
	if(type=="INFO"):
		print bcolors.INFO+text+bcolors.ENDC+"\n"
		return
	if(type=="ERROR"):
		print bcolors.BGRED+bcolors.FGWHITE+bcolors.BOLD+text+bcolors.ENDC
		return
	if(type=="MESSAGE"):
		print bcolors.TITLE+bcolors.BOLD+text+bcolors.ENDC+"\n"
		return
	if(type=="INSECURE_WS"):
		print bcolors.OKRED+bcolors.BOLD+text+bcolors.ENDC
		return
	if(type=="OUTPUT"):
		print bcolors.OKBLUE+bcolors.BOLD+text+bcolors.ENDC+"\n"
		return
	if(type=="OUTPUT_WS"):
		print bcolors.OKBLUE+bcolors.BOLD+text+bcolors.ENDC
		return
	if(type=="SECURE"):
		print bcolors.OKGREEN+bcolors.BOLD+text+bcolors.ENDC
		return


def isNewInstallation():
	if (os.path.exists(rootDir)==False):
		myPrint("Thank you for Installing Firebase Scanner!", "MESSAGE")
		os.mkdir(rootDir)
		return True
	else:
		return False

def isValidPath(apkFilePath):
	global apkFileName
	myPrint("Checking if the APK file path is valid.", "INFO")
	if (os.path.exists(apkFilePath)==False):
		myPrint("Incorrect APK file path found. Please try again with correct file name.", "ERROR")
		print
		exit(1)
	else:
		myPrint("APK File Found.", "INFO")
		apkFileName=ntpath.basename(apkFilePath)

def reverseEngineerApplication(apkFileName):
	global projectDir
	myPrint("Initiating APK Decompilation Process.", "INFO")
	projectDir=rootDir+apkFileName+"_"+hashlib.md5().hexdigest()
	if (os.path.exists(projectDir)==True):
		myPrint("The same APK is already decompiled. Skipping decompilation and proceeding with scanning application.", "INFO")
		return projectDir
	os.mkdir(projectDir)
	myPrint("Decompiling the APK file using APKtool.", "INFO")
	result=os.system("java -jar "+apktoolPath+" d "+"--output "+'"'+projectDir+"/apktool/"+'"'+' "'+apkFilePath+'"'+'>/dev/null')
	if (result!=0):
		myPrint("Apktool failed with exit status "+str(result)+". Please Try Again.", "ERROR")
		print
		exit(1)
	myPrint("Successfully decompiled the application. Proceeding with enumeraing firebase peoject names from the application code.", "INFO")

def findFirebaseProjectNames():
	global firbaseProjectList
	regex='https*://(.+?)\.firebaseio.com'
	for dir_path, dirs, file_names in os.walk(rootDir+apkFileName+"_"+hashlib.md5().hexdigest()):
		for file_name in file_names:
			fullpath = os.path.join(dir_path, file_name)
			for line in file(fullpath):
				temp=re.findall(regex,line)
				if (len(temp)!=0):
					firbaseProjectList=firbaseProjectList+temp
					myPrint("Firebase Instance(s) Found", "INFO")
	if (len(firbaseProjectList)==0):
		myPrint("No Firebase Project Found. Taking an exit!\nHave an nice day.", "OUTPUT")
		exit(0)
def printFirebaseProjectNames():
	myPrint("Found "+str(len(firbaseProjectList))+"Project References in the application. Printing the list of Firebase Projects found.", "OUTPUT")
	for projectName in firbaseProjectList:
		myPrint(projectName, "OUTPUT_WS")
	print 

def scanDarlingScan():
	myPrint("Scanning Firebase Instance(s)", "INFO")
	for str in firbaseProjectList:
		url='https://'+str+'.firebaseio.com/.json'
		try:
			response = urllib2.urlopen(url)
		except urllib2.HTTPError as err:
			if(err.code==401):
				myPrint("Secure Firbase Instance Found: "+str, "SECURE")
				continue
			if(err.code==404):
				myPrint("Project doesnot exist: "+str, "OUTPUT_WS")
				continue     
			else:
				myPrint("Unable to identify misconfiguration for: ", "OUTPUT_WS")
				continue
		except urllib2.URLError as err:
			myPrint("Facing connectivity issues. Please Check the Network Connectivity and Try Again.", "ERROR")
			print 
			continue
		myPrint("Misconfigured Firbase Instance Found: "+str, "INSECURE_WS")
	print

####################################################################################################


####################################################################################################
print(bcolors.INFO+""" 
				@@@@@@@@  @@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@   @@@@@@@@  
				@@!       @@!  @@!  @@@  @@!       @@!  @@@  @@!  @@@  !@@       @@!       
				!@!       !@!  !@!  @!@  !@!       !@   @!@  !@!  @!@  !@!       !@!       
				@!!!:!    !!@  @!@!!@!   @!!!:!    @!@!@!@   @!@!@!@!  !!@@!!    @!!!:!    
				!!!!!:    !!!  !!@!@!    !!!!!:    !!!@!!!!  !!!@!!!!   !!@!!!   !!!!!:    
				!!:       !!:  !!: :!!   !!:       !!:  !!!  !!:  !!!       !:!  !!:       
				:!:       :!:  :!:  !:!  :!:       :!:  !:!  :!:  !:!      !:!   :!:       
				 ::        ::  ::   :::   :: ::::   :: ::::  ::   :::  :::: ::    :: ::::    
				                                                                           
				                                                                      
				 @@@@@@    @@@@@@@   @@@@@@   @@@  @@@  @@@  @@@  @@@@@@@@  @@@@@@@   
				@@@@@@@   @@@@@@@@  @@@@@@@@  @@@@ @@@  @@@@ @@@  @@@@@@@@  @@@@@@@@  
				!@@       !@@       @@!  @@@  @@!@!@@@  @@!@!@@@  @@!       @@!  @@@  
				!@!       !@!       !@!  @!@  !@!!@!@!  !@!!@!@!  !@!       !@!  @!@  
				!!@@!!    !@!       @!@!@!@!  @!@ !!@!  @!@ !!@!  @!!!:!    @!@!!@!   
				 !!@!!!   !!!       !!!@!!!!  !@!  !!!  !@!  !!!  !!!!!:    !!@!@!    
				     !:!  :!!       !!:  !!!  !!:  !!!  !!:  !!!  !!:       !!: :!!   
				    !:!   :!:       :!:  !:!  :!:  !:!  :!:  !:!  :!:       :!:  !:!  
				:::: ::    ::: :::  ::   :::   ::   ::   ::   ::   :: ::::  ::   :::"""+bcolors.OKRED+bcolors.BOLD+"""

                				
                				# Developed By Shiv Sahni - @shiv__sahni
"""+bcolors.ENDC)

if (len(sys.argv)<3):
	myPrint("Please provide the required arguments to initiate scanning.", "ERROR")
	print ""
	myPrint("Usage: python FirebaseMisconfig.py [options]","ERROR")
	myPrint("\t-p/--path <apkPathName>","ERROR")
	myPrint("\t-f/--firebase <commaSeperatedFirebaseProjectName>","ERROR")
	myPrint("Please try again!!", "ERROR") 
	print ""
	exit(1);
if (sys.argv[1]=="-p" or sys.argv[1]=="--path"):
	apkFilePath=sys.argv[2];
	isNewInstallation()
	isValidPath(apkFilePath)
	reverseEngineerApplication(apkFileName)
	findFirebaseProjectNames()
	scanDarlingScan()
if (sys.argv[1]=="-f" or sys.argv[1]=="--firebase"):
	firbaseProjectList=sys.argv[2].split(",")
	isNewInstallation()
	scanDarlingScan()

myPrint("Thank You For Using FireBase Scanner","INFO")