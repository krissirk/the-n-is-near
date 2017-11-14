Python code that enables an Amazon Alexa Skill that announces the predicted times for a local N Muni train stop.

- n.py is a script that pulls in XML data for two  N train route directions at a given stop from webservices.nextbus.com, assembles a message, and prints the message to the console.
- n-lambda.py includes the additional AWS Lambda code that powers the Alexa Skill.

Python Package Dependencies:
- requests
- xmltodict

Follow instructions at http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html to install dependencies within project folder and create a deployment package .zip file that contains all the code required to power the Alexa Skill on AWS Lambda.
