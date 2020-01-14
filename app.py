# tictactoe-for-line/app.py
import os
from decouple import config
from game_func import *
from flask import (
    Flask, request, abort
)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, 
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    FollowEvent, JoinEvent, LeaveEvent
)

app = Flask(__name__)

# get LINE_CHANNEL_ACCESS_TOKEN from your environment variable
line_bot_api = LineBotApi(
    config("LINE_CHANNEL_ACCESS_TOKEN",
           default=os.environ.get('LINE_ACCESS_TOKEN'))
)
# get LINE_CHANNEL_SECRET from your environment variable
handler = WebhookHandler(
    config("LINE_CHANNEL_SECRET",
           default=os.environ.get('LINE_CHANNEL_SECRET'))
)


@app.route("/callback", methods=['POST'])
def callback():
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

NEW_TEXT = ''' Welcome to the Tic-Tac-Toe LINE BOT! 
                To start, simply type \'start\' to start a game of 
                Tic-Tac-Toe, then simply type the position
                (e.g \'1 1\') to place a piece in the board.''' 
FOLLOW_TEXT = 'You can also add me to groups, and play with your friends!'
LEAVE_TEXT = 'Thank you for playing, bye-bye!'
games = []

@handler.add(FollowEvent)
def new_follower(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=NEW_TEXT))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=FOLLOW_TEXT))

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    txt = event.message.text
    if txt == 'start':
        board = start_game()
        output = print_board(board)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=output))
    '''
    if txt == 'start':
        game_num = len(games)
        if isinstance(event.source, SourceUser):
            
        elif isinstance(event.source, SourceRoom) or isinstance(event.source, SourceGroup):
    '''
'''
@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=NEW_TEXT))

@handler.add(LeaveEvent)
def leave_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=LEAVE_TEXT))
'''
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)