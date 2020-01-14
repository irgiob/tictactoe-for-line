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

# stores ongoing games
games = {}

# function gets called whenever the bot recieves a text message
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # gets text message and checks if its a move
    txt = str(event.message.text).lower()
    move = [int(num) for num in txt.split() if num.isdigit()]
    
    if isinstance(event.source, SourceUser):
        # gets userID and starts a new game if text message is start
        userID = str(event.source.user_id)
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
        
        # if a game under that userID has already begun, play or end game
        elif (userID in games):
            if txt == 'end':
                games.pop(userID)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='Game Over. Thanks for playing!'))
            
            # checks if move is valid and sends text if it isn't
            elif len(move) == 2:
                if is_invalid_move(games[userID],move) == 1:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='Out of bounds, try again.'))
                elif is_invalid_move(games[userID],move) == 2:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='Space already filled, try again.'))
                
                # if it is then check if the game is over
                else:
                    games[userID] = play_round(games[userID],1,move)
                    if check_win(games[userID],1) == True or is_full(games[userID]) == True:
                        output = print_board(games[userID])
                        if check_win(games[userID],1) == True:
                            output += 'You win!\nGame Over. Thanks for playing!'
                        elif is_full(games[userID]) == True:
                            output += 'It\'s a tie!\nGame Over. Thanks for playing!'
                        games.pop(userID)
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=output))
                    
                    # if not, let the AI choose a move and check if the game is over again
                    else:
                        AI_move = AI_choose(games[userID])
                        games[userID] = play_round(games[userID],-1,AI_move)
                        if check_win(games[userID],-1) == True or is_full(games[userID]) == True:
                            output = print_board(games[userID])
                            if check_win(games[userID],-1) == True:
                                output += 'AI wins!\nGame Over. Thanks for playing!'
                            elif is_full(games[userID]) == True:
                                output += 'It\'s a tie!\nGame Over. Thanks for playing!'
                            games.pop(userID)
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=output))
                        
                        # if the game is not over, send the updated game board to the user for them to pick their next move
                        else:
                            output = print_board(games[userID])
                            output += f'You picked {move}, AI picked {AI_move}, type \'row col\' where you want to place your next piece.'
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=output))

            # sends a text if text message is not recognized as any command or move
            elif len(move) != 2:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='Invalid Move, type \'row col\' where you want to place your piece.'))            

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)