from flask import Flask, render_template
from flask import request
import urllib.request
import json
import os
import ssl

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def handle_form():
    if request.method == 'POST':
     
     query=request.form.get('user-input')
         # Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
     data = {"query":f"{query}"}

     body = str.encode(json.dumps(data))

     url = 'YOUR_REQUEST_URL_GOES_HERE'
 # Replace this with the primary/secondary key or AMLToken for the endpoint
     api_key = 'YOUR_AUTH_API_KEY_GOES_HERE'
     if not api_key:
      raise Exception("A key should be provided to invoke the endpoint")

 # The azureml-model-deployment header will force the request to go to a specific deployment.
 # Remove this header to have the request observe the endpoint traffic rules
     headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'custom-copilot-initial-1' }

     req = urllib.request.Request(url, body, headers)

     try:
      response = urllib.request.urlopen(req)

      result = response.read()
      result_json = json.loads(result.decode('utf-8'))
      reply = result_json['reply']
      
    
     except urllib.error.HTTPError as error:
      print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
      print(error.info())
      print(error.read().decode("utf8", 'ignore'))
     return render_template('chatbot.html', reply=reply)
    else:
        return render_template('chatbot.html')
    

if __name__ == '__main__':
    app.run()
