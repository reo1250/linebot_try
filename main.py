"""
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import random

app = Flask(__name__)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def myIndex(l,x):
	if x in l:
		return l.index(x)
	else:
		return -1

hands = ["グー","チョキ","パー"]

def hands_to_int(userhand):
	return myIndex(hands,userhand)

def select_bothand():
	return random.randint(0,2)

def judge(userhand,bothand):
	message = []
	if userhand == -1:
		message1 = ["グー、チョキ、パーのうちどれを出しますか?"]
	else:
		status = (userhand - bothand + 3) % 3
		message1 = ["BOTが出したのは" + hands[bothand] + "！"]
		
		if status == 0:
			message1 += ["結果はあいこでした！","もっかい！"]
		elif status == 1:
			message1 += ["結果は負けでした！", "残念…。", "また挑戦してみてね！"]	
		elif status == 2:
			message1 += ["結果は勝ちでした！","おめでとうございます！"]
	return message1

def createMessages(arry):
	messages = arry
	send_messages = []

	for message in messages:
		send_messages.append(TextSendMessage(text=message))

	return send_messages

@app.route("/callback", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']

	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)

	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)

	return 'OK'

@handler.add(MessageEvent, message=TextMessage)


def handle_message(event):
	# message = event.message.text                     <--- コメントアウト
	# message = hands_to_int(event.message.text)       <--- コメントアウト
	# message = select_bothand()                       <--- コメントアウト
	message = judge(hands_to_int(event.message.text), select_bothand())
	line_bot_api.reply_message(
		event.reply_token,
		#TextSendMessage(text=message)
		createMessages(message)
	)


if __name__ == "__main__":
#    app.run()
	port = int(os.getenv("PORT", 5000))
	app.run(host="0.0.0.0", port=port)
"""

import os

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, QuickReplyButton, MessageAction, QuickReply, TextSendMessage)

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def response_message(event):
    hands_list = ["グー", "チョキ", "パー"]

    items = [QuickReplyButton(action=MessageAction(label=f"{hand}", text=f"{hand}")) for hand in hands_list]

    messages = TextSendMessage(text="グー、チョキ、パーのうちどれを出しますか?",
                               quick_reply=QuickReply(items=items))

    line_bot_api.reply_message(event.reply_token, messages=messages)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
#"""
