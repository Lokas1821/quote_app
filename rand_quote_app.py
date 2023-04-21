import redis
import json
from jsonpath_ng import jsonpath, parse
import requests
import random

redis_connection = redis.Redis(
    host='localhost',
    port=6379,
    charset='utf-8',
    decode_responses=True
)

response = requests.get("https://dummyjson.com/quotes")
#list_quote = response.text
quote = json.loads(response.text)
redis_connection.ping()

#print(quote['quotes'][0]['author'])
redis_connection.json().set("my_quotes",'$',response.json())

num_quotes = redis_connection.json().arrlen("my_quotes", "$.quotes")[0]

with open("datafile.json", 'r') as json_file:
    json_data = json.load(json_file)



random_num = random.randint(0, num_quotes)
#random_num = len(json_data["quotes"])
#index = random.randint(0, random_num -1)

def find_quote():
    capture = redis_connection.json().get("my_quotes", f"$.quotes[{random_num}]")[0]
    captured_quote = capture.get('quote')
    captured_author = capture.get('author')
    print(f'random quote: {captured_quote} Author: {captured_author}')

def rand_quote():
    get_quote = input("If you would like a random quote, type 'y' and enter: ")
    if get_quote == 'y':
        find_quote()
    else:
        pass

def add_quote():
    add_quote = input("If you would like to add your own quote, type 'y' and enter: ")
    if add_quote == 'y':
        new_quote = input("Please enter your quote followed by enter: ")
        new_author = input("Please enter your name followed by enter: ")
        print("Thank you for your input!")
    else:
        pass
    redis_connection.set(new_quote, new_author)

rand_quote()
add_quote()
find_quote()
