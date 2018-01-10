Python code that enables an Amazon Alexa Skill that announces the predicted times for a local N Muni train stop...and submits an SMS via Twilio.

- n.py is a script that pulls in XML data for two  N train route directions at a given stop from webservices.nextbus.com, assembles a message, and prints the message to the console. It also takes that message and submits an SMS to my phone, along with a link to request more updated information at Nextbus.
- n-lambda.py includes the additional AWS Lambda code that powers the Alexa Skill.

The code would definitely benefit from some more defensive logic and checks due to the variability of the XML data and structure, but it works well enough to enable my first Alexa Skill (and play around with Twilio's Python Helper Library SDK)!!!

Python Package Dependencies:
- requests
- xmltodict
- Twilio

Follow instructions at http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html to install dependencies within project folder and create a deployment package .zip file that contains all the code required to power the Alexa Skill on AWS Lambda.
