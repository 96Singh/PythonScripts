#! /usr/bin/python3
# DiceGuessingGame
#Simple and fun dice game.

from random import randint
result = (randint(1, 6))
guess = input('Guess which number the dice lands on???: ')
try:
	if int(guess) == result:
		print('Yep, you guessed right!')
	else:
		while int(guess) != result:
			print('Sorry, the value you guessed is wrong!\n')
			guess = input('Guess which number the dice lands on???: ')
			if int(guess) == result:
				print('Yep, you guessed right!')
				break
except:
	print('\nPlease enter a number when you next run the script.')