import os
import openai

openai.api_key = os.getenv("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")

# response = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {
#       "role": "user",
#       "content": "A string de-duplication function in python is implemented in C++ and compiled into a dynamic link library that calls the function in a python script. python passes a string to a C++ function, and C++ returns the de-duplicated string to python after removing the duplicate characters. How to achieve, please write a case."
#     }
#   ],
#   temperature=1,
#   max_tokens=256,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0
# )


import requests

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = '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'

# Example URL of the API
url = 'https://api.example.com/endpoint'

# Example payload (parameters to be sent with the request)
payload = {
    'param1': 'value1',
    'param2': 'value2'
}

# Header containing the API key
headers = {
    'API-Key': API_KEY,
    'Content-Type': 'application/json'  # Adjust content type based on the API's requirements
}

# Making a GET request to the API
response = requests.get(url, headers=headers, params=payload)

# Checking the response
if response.status_code == 200:
    data = response.json()
    print(data)  # Process the received data as per the API's response format
else:
    print("Request failed with status code:", response.status_code)
