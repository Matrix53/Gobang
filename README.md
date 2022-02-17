# Gobang

## Introduction
This repo implement a Gobang game as my homework to a BUAA programing course. The game will be written in python and use modules like pygame, sqlite3 and etc. All are welcome to enjoy the game or improve it after I finish my homework. And of course you can help me with my homework if you want. ( :

## Requirement

### Basic Requirement

> 1.Play Gobang game in one PC
>
> 2.Get the rules of Gobang before play(deleted)

### Extra Requirement

These requirements are challenging for me to implement because of the homework time limit, but I will try my best.

> 1.Use SQLite3 to record the Gobang games that players played
>
> 2.Provide some epic endgame to improve players' Gobang level(deleted)
>
> 3.Use socket to help players playing in LAN
>
> 4.Create a Gobang AI to play with players
>
> 5.Offer some video about Gobang to players

## Development

### Environment

> python:3.7.8
>
> pygame:1.9.6
>
> lxml:4.5.0
>
> beautifulsoup4:4.8.2
>
> requests:2.22.0
>
> Editor:VScode1.48.2
>
> System:Windows10

If you want to produce a program with postfix '.exe', you may need:

> pyinstaller:4.0
>
> pywin32:228

### Code Structure

>Chess.py:include the chess class
>
>Utility.py:include some universal function
>
>Main.py:include the main function, the game starts here
>
>StartGame.py:just used to print the main menu
>
>PlayInOnePc.py:implement the function of playing in one PC
>
>PlayInLAN.py:implement the function of playing in LAN or WLAN
>
>PlayWithAI.py:implement the function of playing with AI
>
>WatchVideo.py:implement the function of watching video through browser
>
>ReviewHistory.py:implement the function of reviewing the play history

## Known Problems

> 1.(PlayInLAN mode)Because the program uses UDP to communicate, player may wait the opponent to operate. In this case, the program will be unresponsive.
>
> 2.(all mode)Because the program doesn't clear the queue of pygame.event, some unexpected operation may be left in the queue which can cause trouble.
>
> 3.(PlayWithAI mode)Because of the time limit of my homework, the IQ of the AI is very low.
