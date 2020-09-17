# playcards
## Introduction
A Chinese card game (Running Fast) implement with python.<br>

## Server Setting
Because we haven't set a public server, so you may not able to play with your friends in WAN.<br>
However, you can still play in a LAN.<br>
Below are the reference settings.<br>
1. Download
```
$ git clone https://github.com/James-yaoshenglong/playcards.git
```
2. Start
```
$ cd src && python3 networkServer.py
```
Then keep the server program running until you finish the game.<br>

## Starting Play 
1. Preparation
```
$ pip install pygame
```
2. Download
```
$ git clone https://github.com/James-yaoshenglong/playcards.git
```
3. Client Setting
```
$ vim src/networkClient.py
```
Then change the bind ip to your server ip.<br>
4. Start
```
$ cd src && python3 main.py
```

