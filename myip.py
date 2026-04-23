import requests


def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        data = response.json()
        return data["ip"]
    except Exception as e:
        print(f"Error fetching public IP: {e}")
        return None


if __name__ == "__main__":
    print(get_public_ip())
# 150.249.252.73
