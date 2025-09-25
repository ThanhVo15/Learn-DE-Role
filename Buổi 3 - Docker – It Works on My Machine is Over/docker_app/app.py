import requests
import os

def get_lastest_bitcoin_price():
    try:
        url = os.getenv("API_URL")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        price = data["1forge.com"]["preferred"]
        print(f"Current Bitcoin Price (USD): {price}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: Test Gen2")

if __name__ == "__main__":
    get_lastest_bitcoin_price()