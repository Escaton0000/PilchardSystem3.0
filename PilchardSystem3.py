import hgtk
import csv
import time
from flask import Flask, render_template, request, redirect, url_for, session
import copy
import os
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")
wordData='./Fin0.csv'
bwordData='./Fin1.csv'

with open(wordData, "r", encoding="utf-8") as f:
    wordlist = [line.strip() for line in f if line.strip()]


with open(bwordData, "r", encoding="utf-8") as f:
    bwordlist = [line.strip() for line in f if line.strip()]

C=['절대안깸','컹컹이','관둬','놈리건보병','극지사냥꾼워윅','꺄우듬','쿰쿰','떵개떵','또운다또','봅보로봅봅','빛의그릇','뻔뻔','쏘쏘','던지고팡','캣레이디프리미엄에디션','튼튼고기꼬치구이와버섯','펠리슨','핌핌','핏빛달쉔','훔쳐','밈웹','기껏','야릇','뿌듯','빠듯','뻔뻔','캣퍼슨','캣츠']
wordlist=list(set(wordlist)-{'룀힐트'})+C
bwordlist=list(set(bwordlist)-{'룀힐트'})+C
load= bload = wordData = bwordData = loaded_data = bloaded_data = C = 0
basic_rating={}
with open("dict_data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        basic_rating[row["key"]] = int(row["value"])



def rating_update(x,usedpool,Using,letter_rating):
    I=0
    for i in ['읍','댕','찍','잴','쩍','뉘','틱','뚱','겅','껑','쩡','뿍','쓱','괄','굉','꼿','푹','띨','훗','낄','칙','쟉','칭']:
        if i+i in usedpool or x==i:
            letter_rating[i]=[1,31,40,36,31,31,31,10,10,10,10,10,10,4,30,11,15,10,10,5,8,60,-38][I]
        I=I+1    
    if '놈놈' in usedpool or x=='놈' or x=='롬':
        letter_rating['놈']=50
        letter_rating['롬']=33
        letter_rating['족']=-25
        if '섯갈보롬' not in usedpool:
            letter_rating['섯']=-20
        if '션보롬' not in usedpool:
            letter_rating['션']=-25
        if '족은놈' in usedpool and '족은말잣놈' in usedpool:
            letter_rating['족']=14
            letter_rating['션']=78
            letter_rating['섯']=44
            if '롬바르드족' in usedpool:
                letter_rating['션']=letter_rating['섯']=-30
        else:
            if '츠바이그란츠' in usedpool or x=='츠':
                letter_rating['츠']=2

              
    if '둑슨' in usedpool:
        letter_rating['꾼']=letter_rating['넷']=-30
        letter_rating['둑']=19
        
        if '꾼둑꾼둑' in usedpool  and '꾼둑' in usedpool:
            letter_rating['꾼']=89
                        
    if '늠름' in usedpool or x=='름' or x=='늠':
        letter_rating['름']=letter_rating['늠']=81
        letter_rating['뻬']=letter_rating['섶']=20
        letter_rating['늬']=1
        letter_rating['섯']=letter_rating['틀']=letter_rating['층']=-45
        if '틀기름' not in usedpool:
            letter_rating['틀']=-28

    if ('득득' in usedpool or x=='득') and ('촉촉' not in usedpool or '득롱망촉' in usedpool):
        letter_rating['득']=31
    
    if ('흔흔' in usedpool or x=='흔') and (letter_rating['득'] < 0 or '흔득흔득' in usedpool):
        letter_rating['흔']=13
        letter_rating['셜']=-9
    if '촉촉' in usedpool or x=='촉':
        letter_rating['촉']=30
        letter_rating['척']=2
    else:
        if Using=='척족':
            letter_rating['척']=15
        else:
            if '늠름' in usedpool:
                letter_rating['척']=-15
            else:
                letter_rating['척']=12
                if Using == '척골절흔':
                    letter_rating['척']=17
    if '뻑뻑' in usedpool or x=='뻑':
        letter_rating['뻑']=37
        letter_rating['슴']=-69
    if '눅눅' in usedpool or x=='눅' or x=='룩':
        letter_rating['눅']=letter_rating['룩']=33        
    if ('뎅뎅' in usedpool or x=='뎅') and letter_rating['겅']<0:
        letter_rating['뎅']=10
    if '롭플롭' in usedpool or x=='롭':
        letter_rating['롭']=41
    if (x=='늡' or x=='릅') and letter_rating['늠']<0:
        letter_rating['늡']=letter_rating['릅']=35
    if (x=='첩' or '첩첩' in usedpool) and  '첩보원가족' in usedpool:
        letter_rating['첩']=13
    if (x=='톱' or '톱톱' in usedpool) and letter_rating['션']<0 and letter_rating['늬']<0:
        if letter_rating['득']<0:
            letter_rating['톱']=1
        else:
            letter_rating['톱']=-10
    if letter_rating['족']<0:
        if letter_rating['득']<0:
            letter_rating['균']=1
        if letter_rating['름']<0 or "엣지스몰족" in usedpool:
            letter_rating['돔']=-13
            letter_rating['엣']=2
    if letter_rating['돔']<0:
        letter_rating['촙']=81
    if letter_rating['섶']>0:
        letter_rating['눙']=letter_rating['룽']=-40

    
    
    

def endmaqjqclr(x):
    if x=='ㅎ':
        return(['ㅎ'])
    else:
        cho, joong, jong = hgtk.letter.decompose (x)
        if cho == 'ㄹ' and joong in ['ㅑ','ㅕ','ㅛ','ㅠ','ㅖ','ㅒ','ㅣ']:
             return ([hgtk.letter.compose('ㄹ',joong,jong),hgtk.letter.compose('ㅇ',joong,jong)])
        elif cho=='ㄹ' and joong not in ['ㅑ','ㅕ','ㅛ','ㅠ','ㅖ','ㅒ','ㅣ']:
            return ([hgtk.letter.compose('ㄹ',joong,jong),hgtk.letter.compose('ㄴ',joong,jong)])
        elif cho == 'ㄴ' and joong in ['ㅑ','ㅕ','ㅛ','ㅠ','ㅖ','ㅒ','ㅣ']:
            return ([hgtk.letter.compose('ㄴ',joong,jong),hgtk.letter.compose('ㅇ',joong,jong)])
        else:
            return([x])
        
import random

def wordselection(x,usedpool,Using,letter_rating):
    rating_update(x,usedpool,Using,letter_rating)
    candidates = endmaqjqclr(x)   
    botpool = []
    for c in candidates:
        words_for_c = [
            w for w in bwordlist 
            if isinstance(w, str) and w.startswith(c)
        ]
        botpool.extend(words_for_c)
    botpool = [w for w in botpool if w not in usedpool]

    if not botpool:
        return None
    scored = []
    for w in botpool:
        last_char = w[-1]
        score = letter_rating.get(last_char, 0)
        scored.append((w, score))

    max_score = max(score for _, score in scored)
    candidates_max = [w for w, score in scored if score == max_score]
    best_word = random.choice(candidates_max)
    return best_word
    

@app.route("/", methods=["GET", "POST"])
def index():
    letter_rating = basic_rating.copy()
    if 't' not in session:
        session['t'] = random.choice(wordlist)
        session['usedpool'] = [session['t']]
    t = session['t']
    usedpool = session['usedpool']
    Using = request.form.get("text")

    if Using in wordlist and Using not in usedpool:
        if Using[0] in endmaqjqclr(t[-1]):
            usedpool.append(Using)
            next_word = wordselection(Using[-1], usedpool, Using, letter_rating)
            if next_word:
                usedpool.append(next_word)
                t = next_word
                session['t'] = t
            session['usedpool'] = usedpool

    return render_template("s.html", messages=usedpool)


@app.route("/reset", methods=["GET"])
def reset():
    session.clear()
    time.sleep(0.7)
    return redirect(url_for("index"))


@app.route("/info", methods=["GET"])
def info():
    return render_template("info.html")

@app.route("/back", methods=["POST"])
def back():
    return redirect(url_for("index"))

@app.route("/start", methods=["GET","POST"])
def start():
    if request.method == "POST":
        if request.form.get("text") in wordlist:
            session["t"] = request.form.get("text")
            session["usedpool"] = [session["t"]]
            print(session["t"])
        return redirect(url_for("index"))
        
    else:
        return render_template("start.html")

if __name__ == "__main__":
    app.run(debug=True)

      

