import requests

API_token = "hehe"
API_Link = "https://api.telegram.org/bot{API_token}"

updates = requests.get(
    API_Link.format(API_token=API_token) + "/getUpdates?offset=-1"
).json()

print(updates)

message = updates["result"][0]["message"]
chat_id = message["from"]["id"]
chat_id_daniel = "pupu"
text = message["text"]

print(text)

desired_text = "я могу тебе писать теперь АХАХААХАХАх"
send_message = requests.get(
    API_Link.format(API_token=API_token)
    + f"/sendMessage?chat_id={chat_id_daniel}&text={desired_text}"
)


def sum_word(word_1: str, word_2: str):
    return word_1 + word_2


print("push, jandos")
