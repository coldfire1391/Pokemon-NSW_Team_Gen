#!usr/bin/python3

# I want a program that will give me all possible 6-teams that share no weaknesses
# input will be a .csv file (excel spreadsheet). An adjacency matrix with edges representing shared-wekaness
# output will be a text file with this format:
# Team 1
# <type1>, <type2>, <type3>, <type4>, <type5>, <type6>

# normal	fighting	flying	poison	ground	rock	bug	ghost	steel	fire	water	grass	electric	psychic	ice	dragon	dark	fairy

import random
import numpy as np
import pandas as pd



# number to type <array>
NTT = ["normal","fighting","flying","poison","ground","rock","bug","ghost","steel","fire","water","grass","electric","psychic","ice","dragon","dark","fairy"]

# type to number <dictionary>
TTN = {"normal":0, "fighting":1, "flying":2, "poison":3, "ground":4, "rock":5, "bug":6, "ghost":7, "steel":8, "fire":9, "water":10, "grass":11, "electric":12, "psychic":13, "ice":14, "dragon":15, "dark":16, "fairy":17}



def comp_check(swm, fmem):
	return not (swm[fmem[1]][fmem[0]] | swm[fmem[2]][fmem[0]] | swm[fmem[3]][fmem[0]] | swm[fmem[4]][fmem[0]] | swm[fmem[2]][fmem[1]] | swm[fmem[3]][fmem[1]] | swm[fmem[4]][fmem[1]] | swm[fmem[3]][fmem[2]] | swm[fmem[4]][fmem[2]] | swm[fmem[4]][fmem[3]])

def powerset(swm, fmemlist, s):
	x = len(s)
	for i in range(1 << x):
		Fmem = [s[j] for j in range(x) if (i & (1 << j))]
		if len(Fmem) == 5 and comp_check(swm, Fmem):
			# print(Fmem)
			fmemlist.append(Fmem)
	return



SWM = pd.read_csv("SWM.csv").to_numpy() # it is now a matrix
# print(SWM)

f = open("output.txt", "w")

cont = "y"
while cont == "y":
	# mandatory type <static variable>
	mtype = TTN[input("Please input one Type you wish to have on your team: ").lower()]
	f.write(NTT[mtype]+"\n")

	# potential members <array>
	Pmem = [p for p in range(0,18) if SWM[mtype][p] == 0] # or p == mtype
	print(Pmem)

	FmemList = []

	powerset(SWM, FmemList, Pmem)
	final_output = [str([NTT[z] for z in w])+"\n" for w in FmemList]

	f.writelines(final_output)
	f.write("\n")

	cont = input("Would you like to use a different Type? [Y/N]: ").lower()

f.close()