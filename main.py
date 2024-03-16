import requests

API_token = "-"
API_Link = "https://api.telegram.org/bot{API_token}"

updates = requests.get(
    API_Link.format(API_token=API_token) + "/getUpdates?offset=-1"
).json()


# print(updates)

# message = updates["result"][0]["message"]

# chat_id = message["from"]["id"]
# chat_id_daniel = "-"
# chat_id_zhandos = "-"
# text = message["text"]


# desired_text = "Привет, коллегеа"
# send_message = requests.get(
#     API_Link.format(API_token=API_token)
#     + f"/sendMessage?chat_id={chat_id_zhandos}&text={desired_text}"
# )
