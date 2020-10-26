import requests
import numpy as np


BASE = "http://127.0.0.1:3001/"
# BASE = "https://capstone-2021.herokuapp.com/"

# response = requests.patch(BASE + "2", {"txt": "whatthefuck"})
# print(response.json())


data = [{"News_url": 'https://www.cnbc.com/2020/10/16/more-volatility-is-likely-ahead-as-rising-cases-lack-of-stimulus-overshadow-strong-earnings.html'},
        {"News_url": 'https://vnexpress.net/mien-trung-so-tan-hon-90-000-dan-102-nguoi-chet-4179085.html'},
        {"News_url": 'https://www.cnbc.com/2020/10/16/more-volatility-is-likely-ahead-as-rising-cases-lack-of-stimulus-overshadow-strong-earnings.html'},]
        

print("Test 1: put response")

for i in range(len(data)):
    response = requests.put(BASE + str(np.random.randint(10000)), data[i])
    print(response.json())

# print("Test 2: get response")

# response = requests.get(BASE + "1")
# print(response.json())

# print("Test 3: not existed")

# response = requests.get(BASE + "9")
# print(response.json())

# print("Test 4: delete")

# response = requests.delete(BASE + "0")
# print(response)

