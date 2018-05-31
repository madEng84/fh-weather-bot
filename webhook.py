import json
import os
import requests

from flask import (Flask, request, make_response)

#Flask app should start in global layout
app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    res = makeResponse(req)
    r = make_response(json.dumps(res, indent=4))
    r.headers['Content-Type']="application/json"
    return r

OPENWEATHER_APP_ID = "0962c9bb943af468124b795a3a5023ba" # tester-1


def makeResponse(req):
    """
    inputParams:
    - città
    - data
    outputParams:
    ???
    
    Esempio di richiesta da DialogFlow:
    {"result":{
      "parameters":{
        "geo-city":"Los Angeles",
        "date":"10/10/2018"
      }
    }}

    Esempio di Risposta:
    {
      "speech":"",
      "displayText":"",
      "source":""
    }
    """
    result = req.get('result')
    parameters = result.get('parameters')
    city = parameters.get('city')
    date = parameters.get('date')
    return get_weather(city,date)

def get_weather(city, date):
    weather_condition = OpenWeather().get_weather(city, date)
    speech = "The forecast for"+city+" for "+date+"is "+condition
    return {
        "speech":speech,
        "displatText":speech,
        "source":"frankhood-weather-webhook"
    }

class DateError(Exception):
    pass
class OpenWeatherError(Exception):
    pass


class OpenWeather(object):
    app_id=OPENWEATHER_APP_ID
    icon_base_url = "http://openweathermap.org/img/w/"#01d.png

    def get_weather(city, date):
        try:
            r = requests.get("http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={app_id}"
                         "".format(app_id=OPENWEATHER_APP_ID,
                                   city_name=city))
            json_r = r.json()
            response_code = json_r['cod']
            if int(response_code) == 200:
                weathers = json_r['list']
                # for i in range(30):
                #    if date in weathers[i]['dt_txt']:
                #        condition = weather[i]['weather'][0]['description']
                #        icon_url = self.icon_base_url + weather[i]['weather'][0]['icon']
                #        return conditon
                for _weather in weathers:
                    if date in _weather['dt_txt']:
                        condition = _weather['weather'][0]['description']
                        icon_url = self.icon_base_url + _weather['weather'][0]['icon']
                        return conditon
                raise DateError("No results for this date")
            else:
                raise OpenWeatherError("Exception Calling OpenWeather : response code was "+response_code)
        except Exception as ex:
            print(ex)
            raise OpenWeatherError("Exception Calling OpenWeather : "+ex)


                


if __name__=='__main__':
    port = int(os.getenv('PORT',5000))
    print("Starting app on port %d"%port)
    app.run(debug=False, port=port, host="0.0.0.0")