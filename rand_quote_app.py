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



with open("datafile.json", 'r') as json_file:
    json_data = json.load(json_file)


random_num = random.randint(1,29)
def find_quote():
    json_expression = parse('quotes[5].quote')  #I thought adding a the random_num variable as the index number would work
    for match in json_expression.find(json_data):
        print(f'random quote: {match.value}')

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
