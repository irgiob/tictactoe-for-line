# tictactoe-for-line

## intro

A few months ago, I had programmed a Tic-Tac-Toe game in C as a one day coding challenge.
After I had finished it I didn't find a use for it until today.
While thinking of a new project to do, I decided I wanted to build some kind of bot,
and decided to do a bot for the messaging app LINE, since it was an app I used frequently.
After a lot of thinking, I finally came up with the idea of remaking my C Tic-Tac-Toe
game in python, and creating a bot where you can play the game on the app with an AI.

## how it works

The bot basically uses LINE's messaging API to create a channel/account where users can send texts.
The text messages are then sent to a webhook to process the text and send one back to the user.
The game is created using the user's UserID, and all follow up moves texted to play the game use
the user ID to keep track of which game board is being played. Every time the user makes a
(valid) move, it'll register it, check if it causes the game to end, then does the same for an AI
which also makes a move. This keeps going on till the game ends or till the user types 'end' to
end the game.

<p align="center"><img src=images/game_example.jpg alt="Application User Interfact" width=500></p>

## ways to improve
 - Add multiplayer support: allow the bot to be placed in group chats and let people in the group verse each other
 - Improve AI: Add proper AI algorithm instead of having the AI just pick a valid spot randomly
 - Other LINE Bots: The next LINE Bot I want to make is a recreation of the game Spyfall