# 以下を「app.py」に書き込み

import streamlit as st
import openai
from pyngrok import ngrok

st.title("ChatGPT Chatbot")
# APIキーの設定
openai.api_key = "xxxxx"


# セッション内で使用するモデルが指定されていない場合のデフォルト値
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# セッション内のメッセージが指定されていない場合のデフォルト値
if "messages" not in st.session_state:
    st.session_state.messages = []

# 以前のメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーからの新しい入力を取得
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty() # 一時的なプレースホルダーを作成
        full_response = ""
        # ChatGPTからのストリーミング応答を処理
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌") # レスポンスの途中結果を表示
        message_placeholder.markdown(full_response) # 最終レスポンスを表示
    st.session_state.messages.append({"role": "assistant", "content": full_response}) # 応答をメッセージに追加
