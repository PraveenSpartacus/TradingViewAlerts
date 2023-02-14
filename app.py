from flask import Flask, request, render_template
import json
import datetime
  
app = Flask(__name__) #creating the Flask class object   


def getAlertHistory():
    file = open('./history.json', 'r')
    s = file.read()
    file.close()
    JSON = json.loads(s)
    return JSON


def setAlertHistory(JSON):
    file = open('./history.json', 'w')
    file.write(json.dumps(JSON, indent=4))
    file.close()



@app.route('/', methods=['GET', 'POST']) #decorator drfines the   
def home():
    JSON = {
        "status": "This is a GET request",
    }
    if request.method == 'POST':
        data = request.json
        JSON = getAlertHistory()
        date = str(datetime.datetime.now())
        JSON.insert(0,{'date':date, 'content':data})
        setAlertHistory(JSON)
        return {"status": "SUCCESS"}
    return JSON

@app.route('/view-alerts', methods=['GET'])
def view_alerts():
    JSON = getAlertHistory()
    return render_template('view_alerts.html', alerts=JSON)
  
if __name__ =='__main__':  
    app.run(host='0.0.0.0', port=80)  