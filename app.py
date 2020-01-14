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

JOIN_TEXT = 'Welcome to the Tic-Tac-Toe LINE BOT!  To start, simply type \'start\' to start a game of Tic-Tac-Toe, then simply type the position (e.g  \'2 1\') to place a piece in the board.'
LEAVE_TEXT = 'Thank you for playing, bye-bye!'
games = {}

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    txt = str(event.message.text).lower()
    move = [int(num) for num in txt.split() if num.isdigit()]
    user = str(event.source.user_id)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=user))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=txt))
    if isinstance(event.source, SourceUser):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Made it to here!'))
        userID = str(event.SourceUser.user_id)
        if txt == 'start':
            if not (userID in games):
                games[userID] = start_game()
                output = print_board(games[userID])
                output += 'Choose where to put piece \'row col\''
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=output))
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='Game already started.'))
        elif (userID in games):
            if txt == 'end':
                games.pop(userID)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='Game Over. Thanks for playing!'))
            elif len(move) == 2:
                if is_invalid_move(games[userID],move) == 1:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='Out of bounds, try again.'))
                elif is_invalid_move(games[userID],move) == 2:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='Space already filled, try again.'))
                else:
                    games[userID] = play_round(games[userID],1,move)
                    if check_win(board,1) == True or is_full(board) == True:
                        output = print_board(games[userID])
                        games.pop(userID)
                        if check_win(board,1) == True:
                            output += 'You win!\nGame Over. Thanks for playing!'
                        elif is_full(board) == True:
                            output += 'It\'s a tie!\nGame Over. Thanks for playing!'
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=output))
                    else:
                        AI_move = AI_choose(games[userID])
                        games[userID] = play_round(games[userID],-1,move)
                        if check_win(board,-1) == True or is_full(board) == True:
                            output = print_board(games[userID])
                            games.pop(userID)
                            if check_win(board,-1) == True:
                                output += 'AI wins!\nGame Over. Thanks for playing!'
                            elif is_full(board) == True:
                                output += 'It\'s a tie!\nGame Over. Thanks for playing!'
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=output))
            elif len(move) != 2:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='Invalid Move, type \'row col\' where you want to place your piece.'))            

# for multiplayer (later)
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