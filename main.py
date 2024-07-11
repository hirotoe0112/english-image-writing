from openai import OpenAI
import os
import streamlit as st


api_key = st.sidebar.text_input("OpenAI API Key", type="password")
client = OpenAI(api_key=api_key)

# 初期化
if "image_url" not in st.session_state:
    st.session_state.image_url = ""
if "my_answer" not in st.session_state:
    st.session_state.my_answer = ""


def get_problem(theme):
    generated = client.images.generate(
        model="dall-e-2",
        prompt=f"{theme}の一場面を写した写真を生成してください。",
        size="512x512",
        quality="standard",
        n=1,
    )

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


st.title("画像を英文で描写する問題ジェネレーター")

theme = st.selectbox(
    "テーマを選択してください",
    ["学生生活", "旅行", "仕事", "スポーツ", "自然"],
)

if st.button("画像を生成"):
    # 画像を生成ボタンを押されたら、画像も回答もクリアする
    st.session_state.image_url = ""
    st.session_state.my_answer = ""

    with st.spinner("画像を生成中..."):
        # 画像をセッションに保存
        st.session_state.image_url = get_problem(theme)

# 画像がセッションに存在したら、画像と回答用テキストエリアを表示する
if st.session_state.image_url != "":
    # セッションに保存されている画像を表示する
    st.image(st.session_state.image_url)

    st.write("生成された画像を見て、画像を英文で描写してください。")
    # 回答をセッションに保存
    st.session_state.my_answer = st.text_area("英文の回答", height=200)

    if st.button("回答をチェック"):
        with st.spinner("チェック中..."):
            ai_comment = check_answer(
                image_url=st.session_state.image_url, answer=st.session_state.my_answer
            )
            st.write(ai_comment)
