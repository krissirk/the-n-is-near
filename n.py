import requests, xmltodict, datetime
from twilio.rest import Client
from config import *

# Set Twilio auth values and phone numbers from local config
if TWILIO_ACCOUNT_SID:
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    toNumber = TWILIO_TO_NUMBER
    fromNumber = TWILIO_FROM_NUMBER
    client = Client(account_sid, auth_token)
else:
	print("Twilio credentials not found!")
	sys.exit(2)

# Initialize message that Alexa will announce to requestor
predictionMessage = ""

# Cache buster for Nextbus request
timestamp = datetime.datetime.now().timestamp()

### Obtain predictions for the SF N Muni train in both directions at Carl & Cole via Nextbus webservice ###
apiUrl = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictionsForMultiStops&a=sf-muni&stops=N|3909&stops=N|3911"
apiUrl += "&time=" + str(int(timestamp))

try:
    r = requests.get(apiUrl)
    muniDoc = xmltodict.parse(r.text)   # Use xmltodict to convert resulting XML to a Python dictionary

except Exception as err:
    predictionMessage = "Predictions not available due to " + str(err) + " error. Please try again later."
    print(err)

### Assemble message for Alexa by iterating through predictions object ###
try:

    for stops in muniDoc["body"]["predictions"]:

        for directions in stops["direction"]:

            if isinstance(directions, dict):    #If the predictions object is a dictionary, obtain values via relevant XML keys

                predictionMessage += str(directions["@title"]) + ": "
                if (directions["prediction"][0]["@minutes"]):
                    predictionMessage += str(directions["prediction"][0]["@minutes"])
                if (directions["prediction"][1]["@minutes"]):
                    predictionMessage += " and " + str(directions["prediction"][1]["@minutes"]) + " minutes away. "
                else:
                    predictionMessage += ". "

            else:   # Else, need to access the values a different way and then break out of loop

                predictionMessage += str(stops["direction"]["@title"]) + ": "
                if (stops["direction"]["prediction"][0]["@minutes"]):
                    predictionMessage += str(stops["direction"]["prediction"][0]["@minutes"])
                if (stops["direction"]["prediction"][1]["@minutes"]):
                    predictionMessage += " and " + str(stops["direction"]["prediction"][1]["@minutes"]) + " minutes away. "
                else:
                    predictionMessage += ". "
                break

except Exception as err:
    predictionMessage = "Predictions not available due to " + str(err) + " error. Please try again later."
    print(err)

# Print the predictions
print(predictionMessage)

# Assemble JSON to be submitted to Alexa
response = {
    'version': '1.0',
    'response': {
        'outputSpeech': {
            'type': 'PlainText',
            'text': predictionMessage,
        }
    }
}

# Print the JSON for Alexa to speak
print(response)

# Text message as SMS via Twilio, along with link for updated predictions
message = client.messages.create(
    to=toNumber,
    from_=fromNumber,
    body=predictionMessage + " Check latest at https://goo.gl/c2xnx2.")

print(message.sid)
