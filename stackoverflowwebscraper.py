import requests
from bs4 import BeautifulSoup
import json
import re


searchurl = "https://stackoverflow.com/search?q={searchtag}"
questionsurl = "https://stackoverflow.com/questions/"
answerurl = "https://stackoverflow.com{url}"
tagges_url = "https://stackoverflow.com/questions/tagged/{tag}?sort=Newest&edited=true"

def tagged_questions(usertag):
    tagged_response = requests.get(tagges_url.format(tag =usertag))
    parsequestions(tagged_response.text)

def general_questions():
    resp = requests.get(questionsurl)
    data = parsequestions(resp.text)
    return data


def searchquestion(searchtext):
    searchquestionresp = requests.get(searchurl.format(searchtag = searchtext))
    soup = BeautifulSoup(searchquestionresp.text,"html.parser")
    questions = soup.select(".question-summary")
    searchdict = {
        "questions" : []
        }
    for q in questions:
        que = q.select_one('.question-hyperlink').getText()
        url = q.select_one( '.question-hyperlink').get('href')
        votes = q.select_one('.vote-count-post').getText()
        searchdict['questions'].append(
            {
                'question': que,
                'url' : url,
                'votes' : votes
            }
            )
    json_data = json.dumps(searchdict,indent=4) 
    return json_data    

def parsequestions(responsetext):  
    soup = BeautifulSoup(responsetext,"html.parser")  
    questions = soup.select(".question-summary")
    questiondictionary = {
    "questions" : []
    }
    for question in questions:
        q = question.select_one('.question-hyperlink').getText()
        url = question.select_one( '.question-hyperlink').get('href')
        votes = question.select_one('.vote-count-post').getText()
        views = question.select_one('.views').attrs['title']
        questiondictionary['questions'].append(
            {
                'question': q,
                'url' : url,
                'views' : views,
                'votes' : votes
            }
            )
    json_data = json.dumps(questiondictionary,indent=4)    
    return json_data


def get_accepted_answer(answer_url):
    answerresponse = requests.get(answerurl.format(url = answer_url))
    soup = BeautifulSoup(answerresponse.text,"html.parser")  
    answers = soup.select_one(".accepted-answer")
    if answers != None:
        print("Answer :")
        answer = answers.select(".js-post-body")
        print(answer)
    else:
        print("No accepted answer")

def get_all_answers(answer_url):
    answerresponse = requests.get(answerurl.format(url = answer_url))
    soup = BeautifulSoup(answerresponse.text,"html.parser")  
    answers = soup.select(".answer")
    for answer in answers:
        if answer != None:
            print("Answer :")
            ans = answer.select(".js-post-body")
            print(ans[0].find('p'))
            print(ans[0].find('code'))
        else:
            print("No answer yet")


data = searchquestion("python pandas multi-level index getting a particular value")
decoded_data = json.loads(data)
for d in decoded_data['questions']:
    print("Question : ",d['question'])
    get_all_answers(d['url'])
