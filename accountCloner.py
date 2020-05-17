import praw, time
timeOutDuration = 10
from prawcore.exceptions import Forbidden

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

subscribedSubreddits = list(oldReddit.user.subreddits(limit=None)) # fetches the list of subscribed subreddits for the old account

subscribedSubreddits = list(map(str, subscribedSubreddits)) # converts the list into a string type

alreadySubscribedSubreddits = list(newReddit.user.subreddits(limit=None)) 

alreadySubscribedSubreddits = list(map(str, alreadySubscribedSubreddits))


for sub in subscribedSubreddits: 
    if sub not in alreadySubscribedSubreddits: # not wasting API calls if the subreddit is already subscribed to
        print('Subscribing to r/' + sub + '..  \n') 
        try: 
            newReddit.subreddit(sub).subscribe() 
        except Forbidden: # if a subreddit is inaccesible or the script times out
            print('Unable to subscribe to r/' + sub + '\n') 
            file = open("subsNotSubscribed.txt","a") 
            file.write(sub +'\n') # the names of the subs are written to a text file
            file.close()
            time.sleep(30) # pauses the script for 30 seconds in case of an API time out
        time.sleep(timeOutDuration) # pausing the script for some duration to prevent a time out

