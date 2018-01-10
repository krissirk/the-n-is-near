import requests, xmltodict, datetime, os
from twilio.rest import Client

# Initialize message that Alexa will announce to requestor
predictionMessage = ""

# Set Twilio auth values and phone numbers, retreiving values from AWS Lambda environment variables
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
toNumber = os.environ.get("TWILIO_TO_NUMBER")
fromNumber = os.environ.get("TWILIO_FROM_NUMBER")

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

# Send SMS with train info via Twilio
message = client.messages.create(
    to=toNumber,
    from_=fromNumber,
    body=predictionMessage + " Check latest at https://goo.gl/c2xnx2.")

# Lambda function that powers Alexa skill
def lambda_handler(event, context):

    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': predictionMessage,
            }
        }
    }

    return response
