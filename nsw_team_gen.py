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



# def comp_check(swm, fmem):
# 	return not (swm[fmem[1]][fmem[0]] | swm[fmem[2]][fmem[0]] | swm[fmem[3]][fmem[0]] | swm[fmem[4]][fmem[0]] | swm[fmem[2]][fmem[1]] | swm[fmem[3]][fmem[1]] | swm[fmem[4]][fmem[1]] | swm[fmem[3]][fmem[2]] | swm[fmem[4]][fmem[2]] | swm[fmem[4]][fmem[3]])

def ccz(swm, fmem, x, y):
	if x == 1:
		return swm[fmem[x]][fmem[0]]
	elif y == -1:
		return ccz(swm, fmem, x-1, x-2)
	else:
		return (swm[fmem[x]][fmem[y]] | ccz(swm, fmem, x, y-1))

def powerset(swm, pmem, lenm, ts, fmemlist):
	x = len(pmem)
	for i in range(1 << x):
		Fmem = [pmem[j] for j in range(x) if (i & (1 << j))]
		if len(Fmem) == (ts-lenm) and not ccz(swm,Fmem,len(Fmem)-1,len(Fmem)-2):
				fmemlist.append(Fmem)
	return



SWM = pd.read_csv("SWM.csv").to_numpy() # it is now a matrix

# creates and writes to the output file
f = open("output.txt", "w")

cont = "y"
while cont == "y":
	# team size
	tsize = int(input("Input desired team size: "))

	# mandatory type <array>
	Mtypes = sorted([TTN[t] for t in input("Input the types you wish to have on your team, separated by comma ','\n (6 MAX): ").lower().split(",")])
	# print("Mtypes: ",Mtypes)
	
	# obtain length of Mtypes
	len_m = len(Mtypes)
	# print("len_m: ",len_m)

	# extend length of Mtypes to 6
	while len(Mtypes) < 6:
		Mtypes.append(Mtypes[0])
	# print("Mtypes: ",Mtypes)

	for x in range(len_m):
		f.write(NTT[Mtypes[x]]+" ")
	f.write("\n")

	# potential members <array>
	Pmem = [p for p in range(0,18) if (SWM[Mtypes[0]][p] == 0 | SWM[Mtypes[1]][p] == 0 | SWM[Mtypes[2]][p] == 0 | SWM[Mtypes[3]][p] == 0 | SWM[Mtypes[4]][p] == 0 | SWM[Mtypes[5]][p] == 0)] # or p == mtype
	print(Pmem)

	FmemList = []

	powerset(SWM, Pmem, len_m, tsize, FmemList)
	final_output = [str([NTT[z] for z in w])+"\n" for w in FmemList]

	f.writelines(final_output)
	f.write("\n")

	cont = input("Would you like to use a different Type? [Y/N]: ").lower()

f.close()