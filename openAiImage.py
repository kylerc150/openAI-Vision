#Imports needed to run this code
import openai
from PIL import Image
import io
import base64
import requests

#Key you would need to access your account
openai.api_key = ""

# Opens image at location using pillow - image is now an object representing the image
image = Image.open("images/bird.jpeg")

# Created to store image data
buffer = io.BytesIO()

#image is saved into the buffer in JPEG format, avoids having to write the image to disk - everything is handled in memory 
image.save(buffer, format="JPEG")

# Encodes the byte data into a base64 string (images as plain text), then retrieves the raw byte data from the buffer, converts the encoded image from bytes into a string (needed for embedding it into a json payload)
encodedImage = base64.b64encode(buffer.getvalue()).decode('utf-8')

# data sent by the sender in packets
payload = {
    #Model we are using for this program - other models available on the openAi API website
    "model": "gpt-4o",
    # What the model is going to look at
    "messages": [
        {
            #We are the users role
            "role": "user",
            # This contains image to look at
            "content":  [
                {
                    # Telling the type of object we are showing chatGpt
                    "type": "image_url",
                    # Contains the image
                    "image_url": 
                        {
                            # embedded base64-encoded image using this format
                            "url": f"data:image/jpeg;base64,{encodedImage}"
                        } 
                }
            ]
         
            
        }     
                ],
    # matters for how long our response will be
    "max_tokens": 4000
}

# Sends an HTTP POST request to OpenAI's API, attaching the JSON payload
response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers = {
            "Authorization" : f"Bearer {openai.api_key}"
        },
        json = payload
    )

#Outputs the response object
print(response)
print("\n")

response_json = response.json()

#Attempts to parse the response into JSON format and print the response
print(response_json)
print("\n")

#This will go though the json and grab the content of the response
print(response.json()["choices"][0]["message"]["content"])
