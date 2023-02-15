from flask import Flask, request, render_template
import json
import datetime

app = Flask(__name__) #creating the Flask class object


def getAlertHistory():
    file = open('./TradingViewAlerts/history.json', 'r')
    s = file.read()
    file.close()
    JSON = json.loads(s)
    return JSON


def setAlertHistory(JSON):
    file = open('./TradingViewAlerts/history.json', 'w')
    file.write(json.dumps(JSON, indent=4))
    file.close()



@app.route('/', methods=['GET', 'POST']) #decorator drfines the
def home():
    JSON = {
        "status": "This is a GET request",
    }
    if request.method == 'POST':
        try:
            host, host_url = request.host, request.host_url
            data = request.json
            JSON = getAlertHistory()
            date = str(datetime.datetime.now())
            JSON.insert(0,{'date':date, 'content':data, 'host':host, 'host_url':host_url})
            setAlertHistory(JSON)
            return {"status": "SUCCESS"}
        except Exception as e:
            JSON.insert(0,{'date':date, 'content':str(e), 'host':host, 'host_url':host_url})
            setAlertHistory(JSON)
            return {"status": "ERROR"}
    JSON = getAlertHistory()
    JSON.insert(0,{'date':"now!", 'content':"GET REQUEST"})
    setAlertHistory(JSON)
    return JSON

@app.route('/view-alerts', methods=['GET'])
def view_alerts():
    JSON = getAlertHistory()
    return render_template('view_alerts.html', alerts=JSON)

if __name__ =='__main__':
    app.run(debug=True, port=443)