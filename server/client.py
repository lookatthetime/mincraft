import requests

# Define the base URL of the server
base_url = 'http://localhost:8000'

# Function to send a GET request
def send_get_request():
    endpoint = '/get_endpoint'  # Replace with the file you want to GET
    url = base_url + endpoint
    response = requests.get(url)
    
    # Print the response status code and content
    # print(f"GET Request Response for {url}:")
    # print(f"Status Code: {response.status_code}")
    # print(f"Content:\n{response.text}\n")

    return response

# Function to send a POST request
def send_post_request():
    endpoint = '/post_endpoint'  # Replace with the endpoint you want to POST to
    url = base_url + endpoint
    data = {'key': 'value'}  # Replace with the data you want to POST
    
    response = requests.post(url, data=data)
    
    # Print the response status code and content
    # print(f"POST Request Response for {url}:")
    # print(f"Status Code: {response.status_code}")
    # print(f"Content:\n{response.text}\n")

    return response

# Sending GET and POST requests

send_post_request()
send_get_request()
