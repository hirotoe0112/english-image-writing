from openai import OpenAI
import os
import requests

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


def get_problem(theme):
    generated = client.images.generate(
        model="dall-e-2",
        prompt=f"{theme}の一場面を写した写真を生成してください。",
        size="512x512",
        quality="standard",
        n=1,
    )

    data = requests.get(generated.data[0].url)
    with open("image.jpg", "wb") as f:
        f.write(data.content)
    return generated.data[0].url


def check_answer(image_url, answer):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"私は画像を英文で描写する問題に取り組んでいます。入力された画像に対して私は{answer}と描写しました。正しく描写できているかどうか、英文に誤りがないかなどをチェックし、日本語で解説してください。",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
    )

    return response.choices[0].message.content


image_url = get_problem("学生生活")
my_answer = input(
    "フォルダに生成されたimage.jpgを見て、画像を英文で描写してください。: "
)
ai_comment = check_answer(image_url=image_url, answer=my_answer)
print(ai_comment)
