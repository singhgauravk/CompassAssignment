import requests
import git
import json
import csv
import github

#Method Library - START

###########################################################################
#  Name: getCommitDateList                                                      #
#  Parameters:                                                            # 
#  userName - Github username                                             #
#  authToken - Personal Access Token for the user's GitHub account  #
###########################################################################


def getCommitDateList(userName, authToken):
	commitDateList = []
	from github import Github
	# using an access token	
	g = Github(authToken)
	gitUser = g.get_user() # get User Object using the Personal Access Token
	repos = gitUser.get_repos()	
	for repoIter in repos: #get all repositories for the user
		print(repoIter.size)
		for commitIter in repoIter.get_commits(): #Iterate through all commits on the repository
			if(commitIter.commit.author.name ==userName): #Filter on username
				commitDateList.append(commitIter.commit.author.date) #Append to collection
	commitDateList.sort(reverse=True) #sort collection keeping latest commit dates first
	return commitDateList

	
########3##################################################################
#  Name: processCommitData                                                #
#  Parameters:                                                            # 
#  commitDateList - Collection of commit times                            #
###########################################################################	

def processCommitData(commitDateList):
	commitDateDict = []
	for commitDate in commitDateList:
		commitDateDict.append({"Date":commitDate.date()}) #Append only the date to a dictionary to be used for writing to csv format
	if(len(commitDateList) != 0): 
		# Write to file & display average commit time only if at least one commit exists
		fields = ['Date']  # Define CSV Header row
		with open(filename, 'w', newline='') as csvfile:    
			writer = csv.DictWriter(csvfile, fieldnames = fields)   
			writer.writeheader()  
			writer.writerows(commitDateDict)
		#Calculate average time diff
		prevTime = 0
		sumOfTimeDiff = 0
		commitCount = 1
		for commitDate in commitDateList[:60]: #slice collection to consider only first 60 elements
			if(prevTime != 0):
				timeDiff = abs((prevTime - commitDate).seconds) # get the difference from the previous commit in seconds
				print(prevTime, commitDate, timeDiff)
				sumOfTimeDiff = sumOfTimeDiff + timeDiff
			else:
				prevTime = commitDate
			commitCount = commitCount + 1
		averageDiffInSeconds = sumOfTimeDiff/commitCount
		return averageDiffInSeconds
	else:
		print("Sorry, either the user", userName, "has not made any check-ins yet or the authentication details are incorrect!")

#Method Library - END

#MAIN PROGRAM

#Initialize Variables
N = 60 #No of Commits to be considered
filename = "CompassAssignmentDataExtract.csv" # filename for csv output

#Get username and authentication token from input
print("Please enter username:")
userName = input() # get github username
print("Please enter Personal Access Token for GitHub")
githubtoken = input() #get github auth token

#get collection of commit date/times
commitDateList = getCommitDateList(userName, githubtoken)

if(len(commitDateList) != 0): #if collection length is not zero, proceed to further processing
	averageDiffInSeconds = processCommitData(commitDateList)
	print("Average time between commits =",averageDiffInSeconds, "seconds(i.e.", averageDiffInSeconds/60, "minutes)")
else:
	print("Sorry, no data was found for the user. Please verify your GitHub user name and Personal Access Token before retrying")




	
