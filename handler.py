from openai import OpenAI
import os
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
import requests

client = OpenAI()
app = APIGatewayRestResolver()

topic_id = os.environ["TOPIC_ID"]
typetalk_token = os.environ["TYPETALK_TOKEN"]
system_content = os.environ["SYSTEM_CONTENT"]


def post_typetalk_message(message):
    print(message)
    url = f"https://typetalk.com/api/v1/topics/{topic_id}"
    headers = {"X-TYPETALK-TOKEN": typetalk_token}

    response = requests.post(url, headers=headers, data={"message": message})
    response.raise_for_status()

    return response.json()


@app.post("/api")
def receiveText():
    # Extract the text from the API request

    print(app.current_event)
    text = app.current_event.json_body["message"]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": syntem_content,
            },
            {"role": "user", "content": text},
        ],
    )
    print(completion.choices)

    post_typetalk_message(completion.choices[0].message.content)

    return {"statusCode": 200, "body": completion.choices[0].message}


def handler(event, context):
    return app.resolve(event, context)
