#!/usr/bin/env python

def evaluate(stri):

 	value = 0
 	elastic = 0
 	for i in stri[3::4]:
 		value = value + int(i)
 		if int(i) == 50:
 			elastic = elastic + 1

	if value > 2000:
 		return [-1, value, elastic]
 	else:
 		return [1, value, elastic]



def print_limits_yes(stri, score, value, elastic):
 	if (elastic == 0):
 		j = 1
 		for i in stri[3::4]:
 			shares=int(i)*2000/value
 			print "set_limit:"+stri[j]+":cpu.shares:"+str(shares)
 			j = j + 4
 	else:
 		j = 1
 		for i in stri[3::4]:
 			if int(i) == 50:
 				shares = int(i) + (2000 - value)/elastic
 			else:
 				shares = int(i)
 			print "set_limit:"+stri[j]+":cpu.shares:"+str(shares)
 		j = j + 4



def print_limits_no(stri):
 	j = 1
 	for i in stri[3::4]:
 		shares = int(i)
 		print "set_limit:"+stri[j]+":cpu.shares:"+str(shares)
 		j = j + 4


def main():

 	stri = []
 	while True:
 		try:
 			input = raw_input()
 			inp = input.split(":")
 			stri = stri + inp
 		except(EOFError):
 			break

 	score, value, elastic = evaluate(stri)

 	if score > 0:
 		print "score:1.0"
 		print_limits_yes(stri, score, value, elastic)
 	else:
 		print "score:-1.0"
 		print_limits_no(stri)


if __name__ == "__main__":
     main()
