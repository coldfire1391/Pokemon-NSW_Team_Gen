#!usr/bin/python3

import random
import numpy as np
import pandas as pd

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

def main():
	# number to type <array>
	NTT = ["normal","fighting","flying","poison","ground","rock","bug","ghost","steel","fire","water","grass","electric","psychic","ice","dragon","dark","fairy"]

	# type to number <dictionary>
	TTN = {"normal":0, "fighting":1, "flying":2, "poison":3, "ground":4, "rock":5, "bug":6, "ghost":7, "steel":8, "fire":9, "water":10, "grass":11, "electric":12, "psychic":13, "ice":14, "dragon":15, "dark":16, "fairy":17}

	# Shared Weakness Matrix
	SWM = pd.read_csv("SWM.csv").to_numpy() # it is now a matrix

	# reads from the st_input.txt file
	f1 = open("st_input.txt", "r")

	# team size	
	inputs = f1.readlines()
	# mandatory type <array>
	tsize = int(inputs[0])
	Mtypes = sorted([TTN[t] for t in inputs[1].strip().lower().split(",")])

	f1.close()

	# creates and writes to the output file
	f2 = open("st_output.txt", "w")

	# obtain length of Mtypes
	len_m = len(Mtypes)

	# extend length of Mtypes to 6
	while len(Mtypes) < 6:
		Mtypes.append(Mtypes[0])

	for x in range(len_m):
		f2.write(NTT[Mtypes[x]]+", ")
	f2.write("\n")

	# potential members <array>
	Pmem = [p for p in range(0,18) if (SWM[Mtypes[0]][p] | SWM[Mtypes[1]][p] | SWM[Mtypes[2]][p] | SWM[Mtypes[3]][p] | SWM[Mtypes[4]][p] | SWM[Mtypes[5]][p] == 0)] # or p == mtype

	FmemList = []

	powerset(SWM, Pmem, len_m, tsize, FmemList)
	final_output = [str([NTT[z] for z in w])+"\n" for w in FmemList]

	f2.writelines(final_output)
	f2.write("\n")

	f2.close()

main()