from flask import Flask, render_template, request
import urllib2, json

my_app = Flask(__name__)


@my_app.route('/', methods=['GET', 'POST'])
def root():
    data = "http://mappy.dali.dartmouth.edu/members.json"
    u = urllib2.urlopen(data)
    d = json.loads(u.read())
    display = {}
    pdict = {}
    counter = 0
    while(len(d) > counter):
        person = d[counter]["name"]
        info = {}
        info["url"] = d[counter]["url"]
        info["termsOn"] = d[counter]["terms_on"][0]
        info["iconURL"] = "../static/" + d[counter]["iconUrl"]
        info["message"] = d[counter]["message"]
        info["lat"] = d[counter]["lat_long"][0]
        info["long"] = d[counter]["lat_long"][1]
        if (len(d[counter]["project"]) > 0):
            info["project"] = d[counter]["project"][0]
        else:
            info["project"] = "n/a"
        pdict[person] = info
        counter +=1
    if (request.method =="POST"):
        for person in pdict:
            if (pdict[person]["termsOn"] == request.form["term"]):
                display[person] = pdict[person]
    else:
        display = pdict
    return render_template('home1.html', group = " : all", display = display)



if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
