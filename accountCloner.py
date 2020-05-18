import praw, time
timeOutDuration = 3
from prawcore.exceptions import Forbidden
from praw.models import Submission
oldAccount = 'oldAccount'
# replace oldAccount and oldPassword with your old Reddit account's username and password respectively
# do the same for newAccount and newPassword for your new Reddit account

oldReddit = praw.Reddit(client_id="SI8pN3DSbt0zor",  # 14-character string mentioned just under 'personal use script' 
                     client_secret="xaxkj7HNh8kwg8e5t4m6KvSrbTI", # 27-character string listed adjacent to the secret field
                     password="oldPassword", # password for your old account
                     user_agent="testscript by /u/oldAccount",  
                     username="oldAccount") # your old account's username


newReddit = praw.Reddit(client_id="SI8pN3DSbt0zor", # credentials for your new account
                     client_secret="xaxkj7HNh8kwg8e5t4m6KvSrbTI",
                     password="newPassword",
                     user_agent="testscript by /u/newAccount",
                     username="newAccount")


def cloneSubreddits(): # function for cloning subreddits

    print('Fetching the subreddits from old account..')
    
    subscribedSubreddits = list(oldReddit.user.subreddits(limit=None)) # fetches the list of subscribed subreddits for the old account
    
    print('Fetching the subreddits from new account..')
    
    alreadySubscribedSubreddits = list(newReddit.user.subreddits(limit=None))# fetches the list of subscribed subreddits for the new account



    for sub in subscribedSubreddits: 
        if sub not in alreadySubscribedSubreddits:
            print('Subscribing to r/' + str(sub) + '..  \n') 
            try: 
                newReddit.subreddit(sub).subscribe() 
            except Forbidden: # if a subreddit is inaccesible or the script times out
                print('Unable to subscribe to r/' + str(sub) + '\n') 
                file = open("subsNotSubscribed.txt","a") 
                file.write(str(sub) +'\n') # the names of the subs are written to a text file
                file.close()
                time.sleep(30) # pauses the script for 30 seconds in case of an API time out
            time.sleep(timeOutDuration) # pausing the script for some duration to prevent a time out


def cloneSavedItems(): #function for cloning saved items

    print('Fetching the saved links from old account..')

    
    savedLinks = oldReddit.redditor(oldAccount).saved(limit=None) # fetching the saved links from old account

    for item in savedLinks:
        if isinstance(item, Submission): # checking if the item is a submission or a comment
            try:
                print('Saving submission id = ' + str(item) + '\n')
                newReddit.submission(id=item).save() # saving the item to the new account
            except:
                print('Unable to save post id = ' + str(item) + '\n')
                file = open("itemsNotSaved.txt","a") 
                file.write(str(item) +'\n') # the ids of the items are written to a text file
                file.close()
        else :
            try:
                print('Saving comment id = ' + str(item) + '\n')
                newReddit.comment(id=item).save()
            except:
                print('Unable to save comment id = ' + str(item) + '\n')
                file = open("itemsNotSaved.txt","a") 
                file.write(str(item) +'\n')
                file.close()
            


cloneSubreddits()

cloneSavedItems()
