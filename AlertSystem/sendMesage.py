import requests

# Session object
session = requests.Session()

# Base URL
base_url = 'https://api.afromessage.com/api/send'

# API token
token = 'eyJhbGciOiJIUzI1NiJ9.eyJpZGVudGlmaWVyIjoiNkNjcHh3TWZHVnQ3Vmxvc0lrVWI5SEpCZHVMWG0wc0QiLCJleHAiOjE4OTU5MjU4MDgsImlhdCI6MTczODE1OTQwOCwianRpIjoiOTE1NWYyZDgtZDIyZi00OWMwLTk1YTAtYTNlNTZhNmUxOWYxIn0.CUOBpxYJmLf9LV4ZfbZezAiug_nClNecIztyWDtaoFw'

# Header
headers = {'Authorization': f'Bearer {token}'}

# Request parameters
callback = ''
to = '+251952137167'
message = 'Hey bro'
from_identifier = ''
sender = ''

# Final URL with proper query parameters
url = f'{base_url}?from={from_identifier}&sender={sender}&to={to}&message={message}&callback={callback}'

try:
    # Make request
    result = session.get(url, headers=headers)

    # Check result
    if result.status_code == 200:
        # Request is successful; inspect the JSON response
        json_response = result.json()
        if json_response.get('acknowledge') == 'success':
            # Success
            print('API success')
        else:
            # Failure
            print('API error:', json_response)
    else:
        # HTTP error
        print(f'HTTP error: Code {result.status_code}, Message: {result.text}')
except Exception as e:
    # Handle exceptions (e.g., network issues)
    print('An error occurred:', str(e))
