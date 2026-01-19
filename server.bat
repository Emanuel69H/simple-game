@echo off

:loop
py server/game_server.py -H 127.0.0.1
goto loop