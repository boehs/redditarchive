#region: imports

try:
    from newspaper import Article
except:
    import os
    os.system("pip install newspaper3k")
try:
    import praw
except:
    import os
    os.system("pip install praw")
import re
import re
import time
import config
import requests
from datetime import datetime
import traceback
#endregion
#region: defs
def parsebasic(url):
    article = Article(url)
    article.download()
    article.parse()
    result = re.sub('(AD\n|ad\n|Advertisement\n|advertisement\n|ADVERTISEMENT\n)', '', article.text)
    result = re.sub('\r\r|\n\n|\r\n\r\n', '', result)
    return(result)

def listsubmissions(): 
    if config.show_feed == True:
        print(submission.selftext)
        print("- " + str(submission.author))
        print(submission.subreddit)
        print("---")

def ifrated():
    if config.is_rated == True:
        time.sleep(600)
    else:
        time.sleep(1)
#endregion
reddit = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "NewsBot By u/bobdarobber")
print("finished logging in")

whitelist = []
with open("whitelist.txt", "r") as file:
    for line in file.readlines():
        whitelist.append(line.rstrip('\n'))
file.close()

subreddit = reddit.subreddit("news+politics+bobdarobber+worldnews") # The subs to respond in (syntax ("sub+sub+sub") ie: ("dogs+dog+aww"))

if config.test_online == True:
    testsubmission = reddit.submission(id=config.online_id)
    print("working...")
    now = datetime.now()
    currenttime = now.strftime("%D:%H:%M")
    testsubmission.reply("booted at " + currenttime)
    print("finished. staus=Ok")
while True:
    try:
        for submission in subreddit.stream.submissions(skip_existing=True):
            if submission.saved == False and submission.is_self == False:
                for website in whitelist:
                    if website in submission.url:
                        print(submission.url)
                        article = Article(submission.url)
                        article.download()
                        article.parse()
                        submission.reply(">"+ parsebasic(submission.url)) + """
                        ---
                        bot provided by u/bobdarobber."""
                        submission.save
    except:
        print("oops a error!")
        traceback.print_exc()