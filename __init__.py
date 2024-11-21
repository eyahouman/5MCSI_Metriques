from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #comm3

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("forms.html") 
  
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def mongraphique2():
    return render_template("graphique2.html")

from flask import Flask, jsonify, render_template
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/commits/')
def commits_chart():
    # URL de l'API GitHub
    api_url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    
    # Récupération des données des commits
    response = requests.get(api_url)
    commits_data = response.json()
    
    # Extraction des minutes des commits
    minutes = []
    for commit in commits_data:
        date_string = commit['commit']['author']['date']
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes.append(date_object.minute)
    
    # Compter le nombre de commits par minute
    commits_per_minute = {}
    for minute in minutes:
        commits_per_minute[minute] = commits_per_minute.get(minute, 0) + 1
    
    # Convertir les données en format utilisable par le graphique
    chart_data = [{"minute": minute, "count": count} for minute, count in commits_per_minute.items()]
    
    return render_template('commits.html', data=chart_data)



  
if __name__ == "__main__":
  app.run(debug=True)
