#!/usr/bin/python3

import sys
import time
import random
import os
import sqlite3 as sql
import re
import math
import platform

n = 5
lost = False
swwp = False
score = 0

db = sql.connect("data.db")
cr = db.cursor()
cr.execute("CREATE TABLE IF NOT EXISTS scores ('score')")

sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=25, cols=40))

zone = 	[["#","#","#","#","#","#"],
	 ["#"," "," "," "," ","#"],
	 ["#"," "," "," "," ","#"],
	 ["#"," "," "," "," ","#"],
	 ["#"," "," "," "," ","#"],
 	 ["#","#","#","#","#","#"]]

def read_input():
    try:
        import readchar
        ch = readchar.readkey()
        return ch
    except ImportError:
        ch = input()
        return ch

def p_color(data):
    try:
        from sty import fg, rs
        logvalue = math.log(data) / math.log(2)
        return '\033[1m' + fg(int(logvalue)) + str(data) + fg.rs
    except ImportError:
        return data

def clear():
	if(platform.system() == "Windows"):
		os.system("cls")
	else:
		os.system("clear")

def print_zone():
	global zone
	global n
	global score
	print("                2048\n")
	print("score:",score,"\n")
	for i in range(n+1):
		for j in range(n+1):
			if(zone[i][j] != "#" and zone[i][j] != " "):
				if(zone[i][j]<10):
					print(p_color(zone[i][j]),end="      ",flush=True)
				elif(zone[i][j]<100 and zone[i][j]>10):
					print(p_color(zone[i][j]),end="     ",flush=True)
				elif(zone[i][j]<1000 and zone[i][j]>100):
					print(p_color(zone[i][j]),end="    ",flush=True)
				elif(zone[i][j]<10000 and zone[i][j]>1000):
					print(p_color(zone[i][j]),end="   ",flush=True)
				elif(zone[i][j]<100000 and zone[i][j]>10000):
					print(p_color(zone[i][j]),end="  ",flush=True)
			else:
				if(zone[i][j] == "#"):
					if((i == 0 or i == n) and j < 5):
						print(zone[i][j],end="######",flush=True)
					else:
						print(zone[i][j],end="      ",flush=True)
				else:
					print(zone[i][j],end="      ",flush=True)
		if(i<n):
			print("\n#                                  #"*2)
	print("\nPress 'q' for quit.")

def play():
	global lost
	global swwp
	global db
	while(True):
		swwp = False
		clear()
		print_zone()
		if(lost == True):
			refresh()
			print("You lose...")
			con = str(input("Press any key..."))
			break
		mov = str(read_input())
		if(mov == "4" or mov == "5" or mov == "6" or mov == "8"):
			if(mov == "4"):
				moveleft()
			elif(mov == "6"):
				moveright()
			elif(mov == "8"):
				moveup()
			elif(mov == "5"):
				movedown()
			clear()
			print_zone()
			time.sleep(1/8)
			generate_num()
		elif(mov == "q"):
			break
		else:
			continue

def putnumber(number):
	global n
	global zone
	global lost
	global swwp
	global score
	count = 0
	control = 0
	for i in range(1,n):
		for j in range(1,n):
			if(zone[i][j] == " "):
				count = 1
				break
	for i in range(1,n):
		for j in range(1,n):
			if(zone[i][j] == zone[i+1][j] and zone[i][j] != " "):
				control = 1
				break
			if(zone[i][j] == zone[i][j+1] and zone[i][j] != " "):
				control = 1
				break
	if(count == 1 and swwp == True):
		while(True):
			rnd_3 = random.randint(1,n-1)
			rnd_4 = random.randint(1,n-1)
			if(zone[rnd_3][rnd_4] == " "):
				zone[rnd_3][rnd_4] = number
				break
	elif(swwp == False and count == 0 and control == 0):
		insert_db(db,score)
		lost = True

def generate_num():
	global swwp
	if(swwp == True):
		rnd = random.randint(1,10)
		if(rnd <= 8):
			rnd_2 = random.randint(1,10)
			if(rnd_2 <= 8):
				putnumber(2)
			else:
				putnumber(4)
		else:
			rnd_2 = random.randint(1,3)
			if(rnd_2 == 1):
				putnumber(2)
				putnumber(2)
			elif(rnd_2 == 2):
				putnumber(2)
				putnumber(4)
			else:
				putnumber(4)
				putnumber(4)
	else:
		putnumber(2)

def moveleft():
	global n
	global zone
	global swwp
	global score
	for k in range(1,n):
		for i in range(1,n):
			if(zone[k][i] == " "):
				for j in range(i+1,n):
					if(zone[k][j] != " "):
						swp = zone[k][i]
						zone[k][i] = zone[k][j]
						zone[k][j] = swp
						swwp = True
						break
		for i in range(1,n-1):
			if(zone[k][i] == zone[k][i+1] and zone[k][i] != " "):
				zone[k][i] += zone[k][i+1]
				score += zone[k][i]
				zone[k][i+1] = " "
				swwp = True
		for i in range(1,n):
			if(zone[k][i] == " "):
				for j in range(i+1,n):
					if(zone[k][j] != " "):
						swp = zone[k][i]
						zone[k][i] = zone[k][j]
						zone[k][j] = swp
						break

def moveright():
	global n
	global zone
	global swwp
	global score
	for k in range(1,n):
		for i in range(n-1,1,-1):
			if(zone[k][i] == " "):
				for j in range(i,0,-1):
					if(zone[k][j] != " "):
						swp = zone[k][i]
						zone[k][i] = zone[k][j]
						zone[k][j] = swp
						swwp = True
						break
		for i in range(n-1,1,-1):
			if(zone[k][i] == zone[k][i-1] and zone[k][i] != " "):
				zone[k][i] += zone[k][i-1]
				score += zone[k][i]
				zone[k][i-1] = " "
				swwp = True
		for i in range(n-1,1,-1):
			if(zone[k][i] == " "):
				for j in range(i,0,-1):
					if(zone[k][j] != " "):
						swp = zone[k][i]
						zone[k][i] = zone[k][j]
						zone[k][j] = swp
						break

def movedown():
	global n
	global zone
	global swwp
	global score
	for k in range(1,n):
		for i in range(n-1,1,-1):
			if(zone[i][k] == " "):
				for j in range(i,0,-1):
					if(zone[j][k] != " "):
						swp = zone[i][k]
						zone[i][k] = zone[j][k]
						zone[j][k] = swp
						swwp = True
						break
		for i in range(n-1,1,-1):
			if(zone[i][k] == zone[i-1][k] and zone[i][k] != " "):
				zone[i][k] += zone[i-1][k]
				score += zone[i][k]
				zone[i-1][k] = " "
				swwp = True
		for i in range(n-1,1,-1):
			if(zone[i][k] == " "):
				for j in range(i,0,-1):
					if(zone[j][k] != " "):
						swp = zone[i][k]
						zone[i][k] = zone[j][k]
						zone[j][k] = swp
						break

def moveup():
	global n
	global zone
	global swwp
	global score
	for k in range(1,n):
		for i in range(1,n):
			if(zone[i][k] == " "):
				for j in range(i+1,n):
					if(zone[j][k] != " "):
						swp = zone[i][k]
						zone[i][k] = zone[j][k]
						zone[j][k] = swp
						swwp = True
						break
		for i in range(1,n-1):
			if(zone[i][k] == zone[i+1][k] and zone[i][k] != " "):
				zone[i][k] += zone[i+1][k]
				score += zone[i][k]
				zone[i+1][k] = " "
				swwp = True
		for i in range(1,n):
			if(zone[i][k] == " "):
				for j in range(i+1,n):
					if(zone[j][k] != " "):
						swp = zone[i][k]
						zone[i][k] = zone[j][k]
						zone[j][k] = swp
						break

def refresh():
	global lost
	global score
	score = 0
	lost = False
	for i in range(1,n):
		for j in range(1,n):
			zone[i][j] = " "

def bb_sort(data):
	for i in range(len(data)):
		for j in range(len(data)):
			if(data[i] > data[j]):
				var = data[i]
				data[i] = data[j]
				data[j] = var
	clear()
	print("TOP SCORES")
	if(len(data) <= 10):
		lengg = len(data)
	else:
		lengg = 10
	for i in range(lengg):
		print(i+1,":",data[i])
	return data

def insert_db(db,data):
	cr = db.cursor()
	query = "INSERT INTO scores VALUES ('{}')".format(int(data))
	cr.execute(query)
	db.commit()

def score_info():
	cr = db.cursor()
	query = "SELECT score FROM scores"
	cr.execute(query)
	datas = cr.fetchall()
	for i in range(len(datas)):
		datas[i] = str(datas[i])
		datas[i] = re.sub('[^0-9]','',datas[i])
		datas[i] = int(datas[i])
	bb_sort(datas)

def main():
	global swwp
	menuc = """
            ####################
            #       2048       #
            #1)NEW GAME        #
            #2)RESUME          #
            #3)TOP SCORES      #
            #4)HOW TO PLAY     #
            #0)EXIT            #
            ####################
        """
	while(True):
		swwp = True
		clear()
		print('\033[1m' + menuc)
		ch = str(read_input())
		if(ch == "1"):
			refresh()
			generate_num()
			play()
		elif(ch == "2"):
			play()
		elif(ch == "3"):
			score_info()
			con = str(input("Press any key..."))
		elif(ch == "4"):
			print("Up:8 - Right:6 - Left:4 - Down:5")
			con = str(input("Press any key..."))
		elif(ch == "0"):
			break
		else:
			continue

clear()
main()
