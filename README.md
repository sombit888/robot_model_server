## Installation 
1. Setup Openvla installation libraries,
2. Install Flask ```pip install Flask```
3. Setup ngrok ``` https://download.ngrok.com/linux``` , setup authkey

## To run the server 
1. ```./ngrok http 8000 ```  note the ip address eg.  https://38bb-34-91-40-242.ngrok-free.app
2. ``` python openvla_hosting.py ``` change the model in the hosting

## For the client 
1. Install requests ``` pip install requests ```
 ```
   files = {
    "image": image_bytes  # Image file to be uploaded
}
data = {
    "instruction": instruction_text  # Text instruction
}

# Send a POST request to the API
response = requests.post(url, files=files, data=data) ```

