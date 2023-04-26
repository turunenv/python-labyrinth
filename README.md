# python-labyrinth

## Description

This project was my final project for Aalto University course Y2 on Python programming.
The assignment was to create a program that creates a playable labyrinth on the screen.
The labyrinth is not just basic 2D labyrinth, but includes underpasses, marked by
dotted lines. The user can determine the size of the labyrinth at the start of a game,
and the algorithm then dynamically creates a new labyrinth for the game.

## Features

- Dynamic maze creation
- Underpasses
- Save and start games from files
- Feeling stuck? Ask for a tip!
- Oh, you really are over it, huh. Activate God-mode!

## Contents of the repository

This repo contains the original program code in the src/ folder. It also
contains the original documents related to the project (plans and final document)
that were written in Finnish language.

## Running the program

The program is tested to work on Python 3.8 and PyQt 5.15. Once you have those
installed, clone the repo and run the game with

> cd src/

> python main.py

Alternatively, if you want to run the game in Docker (repo cloned and docker installed):
> docker build -t python-labyrinth .

> docker run --rm -it \
> -v /tmp/.X11-unix:/tmp/.X11-unix \
> -e DISPLAY=$DISPLAY \
> -u qtuser \
> python-labyrinth

### Note

When the game starts, you may need to first press "G" to make the arrow-key
presses register.
