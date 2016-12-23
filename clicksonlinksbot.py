import praw
import re
import sumy
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


import sys
sys.path.insert(0, '../botsinfo/')
from clicksonlinksbotinfo import *
r = praw.Reddit(
    client_id = client_id,
    client_secret = client_secret,
    password = password,
    username = username,
    user_agent="ClicksOnLinksBot 0.1"
)

#r = praw.Reddit('clicksonlinksbot', user_agent='clicksonlinksbot user agent')

#print(praw.helpers)

word = ur'/?u/clicksonlinksbot'
sub = r.subreddit('all')
comments = sub.stream.comments()
count = 0
SENTENCES_COUNT = 10
nameRegex = re.compile(word, flags=re.IGNORECASE)
LANGUAGE ="english" 
#linkRegex = re.compile(ur'\[.*\]\(.*\)')
for comment in comments:
    body = comment.body
    body.encode('UTF-8')
    count += 1
    
    if nameRegex.search(body) is not None:
        if not comment.is_root:
            print("found comment with our name in it")
            parent = r.comment(comment.parent_id[3:])
            links = re.findall(ur'\[.*\]\(.*\)',parent.body)
            response = ''
            num = 1
            for l in links:                               
                print("link: %s" % l)
                sp = l.split("](")
                text = sp[0][1:]
                url = sp[1][:len(sp[1]) - 1]
                try:
                    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
                except Exception as e : 
                    response += str(num) + '.) ' + text + ': ' + url + '\n\n'
                    response += 'Error parsing link, sorry :(\n'
                    #debug exception option
                    response += '\n\n For debugging, exception: ' + str(e)
                else:
                    stemmer = Stemmer(LANGUAGE)
                    summarizer = Summarizer(stemmer)
                    summarizer.stop_words = get_stop_words(LANGUAGE)
                    
                    response += str(num) + '.) ' + text + ': ' + url + '\n\n'
                    print(response)
                    for sentence in summarizer(parser.document, SENTENCES_COUNT):
                        print(sentence._text)
                        response+='\n'
                        
                        response+=sentence._text
                        response += '\n'
                response += '\n\n----------------------\n\n'
                num += 1
            print('comment reply:\n%s' % response)
            try:
                comment.reply(response)
            except Exception as e:
                print('Error posting comment: ' + str(e))


'''
else:
print("not found: %s" % str(count))
'''
'''


for submission in subreddit.hot(limit=5):
    print("Title: ", submission.title)
    print("Text: ", submission.selftext)
    print("Score: ", submission.score)
    print("---------------------------------\n")
'''
