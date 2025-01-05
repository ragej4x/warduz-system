import requests

url = "http://warduz-petshop.unaux.com/config.txt"  # Note the "http" instead of "https"


response = requests.get(url, timeout=10, verify=False)  # Disable SSL verification

