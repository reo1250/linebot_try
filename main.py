
from flask import Flask, request, abort

from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, QuickReplyButton, MessageAction, QuickReply, TextSendMessage,
)

import os
import random
import datetime
app = Flask(__name__)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


dt = datetime.datetime(2020,2,26,5,0,0,0).timestamp()

def judgeTime(time):
	
	if dt < time:
		message = '遅刻'
	
	elif dt == time:
		message = "ジャスト"
	
	elif dt > time:
		message = "順調"

	return message

def createmessage(time):
	
	currenttime = str(datetime.datetime.fromtimestamp(int(float(time))))

	message = currenttime

	return message

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
	time = event.timestamp / 1000 + 9*3600
	message = judgeTime(time)

	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=message))		


if __name__ == "__main__":
#    app.run()
	port = int(os.getenv("PORT", 5000))
	app.run(host="0.0.0.0", port=port)
