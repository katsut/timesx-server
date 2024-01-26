from openai import OpenAI
import os
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
import requests

client = OpenAI()
app = APIGatewayRestResolver()

topic_id = os.environ["TOPIC_ID"]
typetalk_token = os.environ["TYPETALK_TOKEN"]


def post_typetalk_message(message):
    url = f"https://typetalk.com/api/v1/topics/{topic_id}/messages"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {typetalk_token}"
    }
    payload = {
        "message": message
    }

    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()

    return response.json()


@app.post()
def receiveText():
    # Extract the text from the API request

    text = app.current_event.json_body["message"]

    print(text)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a play-by-play person. From a person's soliloquy, you make statements about what that person is doing, like a baseball or horse race play-by-play man. The user will make the comment, so please be sure to give the actual situation of the soliloquy in Japanese in an objective manner.",
            },
            {"role": "user", "content": text},
        ],
    )
    print(completion.choices)

    post_typetalk_message(completion.choices[0].message)

    return {"statusCode": 200, "body": completion.choices[0].message}


def handler(event, context):
    return app.resolve(event, context)
