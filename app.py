import os
#from model.chatbot.kogpt2 import chatbot as ch_kogpt2
from model.chatbot.kobert import chatbot as ch_kobert
#from model.emotion import service as emotion
from util.emotion import Emotion
from util.depression import Depression
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
from kss import split_sentences
from config import *
import mysql.connector
import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
db = mysql.connector.connect(
    host=mysql_host,
    port=mysql_port,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
)
cursor = db.cursor()

Emotion = Emotion()
Depression = Depression()

JOY=['즐거움', '기쁨']
ANXIETY=['감정조절이상','걱정','공포','과민반응','긴장','두려움','무서움','불안감','불쾌감','불편감', '불안']
SAD=['고독감','공허감','괴로움','기분저하','눈물','멍함','무력감','부정적사고','서운함','속상함','슬픔','외로움','우울감','의기소침','의욕상실','자괴감','자살충동','자신감저하','자존감저하',
     '절망감','좌절','창피함','초조함','통제력상실','허무함','힘듦', '우울']
ANGER=['미움','배신감','분노','불만','불신','짜증','화', '분노']
EMBARRASSMENT=['곤혹감','기시감','당황']

@app.route('/')
def hello():
    return "deep learning server is running 💗"


@app.route('/emotion')
def classifyEmotion():
    sentence = request.args.get("s")
    if sentence is None or len(sentence) == 0 or sentence == '\n':
        return jsonify({
            "emotion_no": 2,
            "emotion": "중립"
        })

    result = emotion.predict(sentence)
    print("[*] 감정 분석 결과: " + Emotion.to_string(result))
    return jsonify({
        "emotion_no": int(result),
        "emotion": Emotion.to_string(result)
    })


@app.route('/diary')
def classifyEmotionDiary():
    sentence = request.args.get("s")
    if sentence is None or len(sentence) == 0 or sentence == '\n':
        return jsonify({
            "joy": 0,
            "hope": 0,
            "neutrality": 0,
            "anger": 0,
            "sadness": 0,
            "anxiety": 0,
            "tiredness": 0,
            "regret": 0,
            "depression": 0
        })

    predict, dep_predict = predictDiary(sentence)
    return jsonify({
        "joy": predict[Emotion.JOY],
        "hope": predict[Emotion.HOPE],
        "neutrality": predict[Emotion.NEUTRALITY],
        "anger": predict[Emotion.ANGER],
        "sadness": predict[Emotion.SADNESS],
        "anxiety": predict[Emotion.ANXIETY],
        "tiredness": predict[Emotion.TIREDNESS],
        "regret": predict[Emotion.REGRET],
        "depression": dep_predict
    })


@app.route('/chatbot/g')
def reactChatbotV1():
    sentence = request.args.get("s")
    if sentence is None or len(sentence) == 0 or sentence == '\n':
        return jsonify({
            "answer": "듣고 있어요. 더 말씀해주세요~ (끄덕끄덕)"
        })

    answer = ch_kogpt2.predict(sentence)
    return jsonify({
        "answer": answer
    })


@app.route('/chatbot/b')
def reactChatbotV2():
    sentence = request.args.get("s")
    if sentence is None or len(sentence) == 0 or sentence == '\n':
        return jsonify({
            "answer": "듣고 있어요. 더 말씀해주세요~ (끄덕끄덕)"
        })

    answer, category, desc, softmax = ch_kobert.chat(sentence)

    if(desc[0:2]=="감정"):
        store_emotion(desc.split('/')[1])
    return jsonify({
        "answer": answer,
        "category": category,
        "category_info": desc
    })

def store_emotion(category_info):
    data = request.json
    emotion = category_info
    current_datetime = datetime.datetime.now()
    current_month = current_datetime.month
    current_year = current_datetime.year

    if emotion in ANGER:
        emotion="anger"
    elif emotion in SAD:
        emotion="sad"
    elif emotion in JOY:
        emotion="joy"
    elif emotion in ANXIETY:
        emotion="anxiety"
    elif emotion in EMBARRASSMENT:
        emotion="embarrassment"
    else:
        emotion="nothing"

    if emotion=='nothing':
        return

    print(emotion)
    
    select_query = "SELECT * FROM emotions3 WHERE (month)= %s AND (year)=%s AND (emotion) = %s"
    cursor.execute(select_query, (current_month,current_year,emotion))
    results = cursor.fetchall()
    count=results[0][3]


    update_query = "UPDATE emotions3 SET count=%s WHERE month= %s AND year=%s AND emotion = %s;"
    cursor.execute(update_query, (count+1,current_month,current_year,emotion))
    db.commit()

#@app.route('/emotions', methods=['GET', 'POST'])
#def inquire_emotions():
#    select_query = "SELECT * FROM emotions ORDER BY date DESC"
#    cursor.execute(select_query)
#    results = cursor.fetchall()

#    emotions = []
#    for row in results:
#        date = row[1]
#        emotion = row[2]
#        emotions.append({'date': date, 'emotion': emotion})

#    return jsonify(emotions)

@app.route('/emotions/count', methods=['GET', 'POST'])
def count_emotions():
    month= request.args.get('month') # 월별 데이터를 조회하기 위한 매개변수
    select_query = "SELECT * FROM emotions3"
    cursor.execute(select_query)
    results = cursor.fetchall()

    emotions = []
    emotions_count= []
    anger, sad, joy, embarrassment, anxiety=0,0,0,0,0
    for row in results:
        month=row[1]
        emotion = row[2]
        count= row[3]
        emotions.append({'month': month, 'emotion': emotion, 'count': count})
    
    for entry in emotions:
        if entry['emotion'] == 'anger':
            anger+=entry['count']
        elif entry['emotion'] == 'sad':
            sad+=entry['count']
        elif entry['emotion'] == 'joy':
            joy+=entry['count']
        elif entry['emotion'] == 'anxiety':
            anxiety+=entry['count']
        elif entry['emotion'] == 'embarrassment':
            embarrassment+=entry['count']
    emotions_count.append({'분노':anger, '우울': sad,
                           '기쁨':joy, '불안':anxiety, '당황':embarrassment})

    return jsonify(emotions_count)

@app.route('/emotions/count/month', methods=['GET', 'POST'])
def count_emotions_month():
    data = request.get_json()  # Get the JSON data from the request body
    month = data.get('month')  # Retrieve the 'month' value from the JSON data
    select_query = "SELECT * FROM emotions3 WHERE month = %s"
    cursor.execute(select_query, (month,))
    results = cursor.fetchall()

    emotions = []
    emotions_count = []
    anger, sad, joy, embarrassment, anxiety = 0, 0, 0, 0, 0
    for row in results:
        month=row[1]
        emotion = row[2]
        count= row[3]
        emotions.append({'month': month, 'emotion': emotion, 'count': count})

    for entry in emotions:
        if entry['emotion'] == 'anger':
            anger+=entry['count']
        elif entry['emotion'] == 'sad':
            sad+=entry['count']
        elif entry['emotion'] == 'joy':
            joy+=entry['count']
        elif entry['emotion'] == 'anxiety':
            anxiety+=entry['count']
        elif entry['emotion'] == 'embarrassment':
            embarrassment+=entry['count']

    emotions_count.append({'분노': anger, '우울': sad, '기쁨': joy, '불안': anxiety, '당황': embarrassment, '월':month})

    return jsonify(emotions_count)


def predictDiary(s):
    total_cnt = 0.0
    dep_cnt = 0
    predict = [0.0 for _ in range(8)]
    for sent in split_sentences(s):
        total_cnt += 1
        predict[emotion.predict(sent)] += 1
        if emotion.predict_depression(sent) == Depression.DEPRESS:
            dep_cnt += 1

    for i in range(8):
        predict[i] = float("{:.2f}".format(predict[i] / total_cnt))
    dep_cnt = float("{:.2f}".format(dep_cnt/total_cnt))
    return predict, dep_cnt


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
