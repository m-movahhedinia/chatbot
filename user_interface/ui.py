# -*- coding: utf-8 -*-
"""
Created on March 03, 2024

@author: mansour
"""

import gradio as gr
import random
import time
from requests import post

url = "http://0.0.0.0:2023/converse/ask"


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(height=1000)
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        bot_message = query_question(message, chat_history)["response"]
        chat_history.append((message, bot_message))
        return message, chat_history

    def query_question(message, chat_history):
        if chat_history:
            chat_history = "\n".join([f"USER: {chat[0]}\nBOT: {chat[1]}" for chat in chat_history])
        else:
            chat_history = None

        payload = {"question": message, "history": chat_history}
        headers = {'Content-Type': 'application/json'}

        response = post(url, headers=headers, json=payload)

        return response.json()


    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch()
