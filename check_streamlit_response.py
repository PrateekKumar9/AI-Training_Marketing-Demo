import urllib.request

with urllib.request.urlopen('http://127.0.0.1:8501') as response:
    html = response.read(1000).decode('utf-8', errors='replace')
    print(html)
