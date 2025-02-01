import requests

def fetch_google():
	response = requests.get("https://www.google.com")
	return response.status_code

