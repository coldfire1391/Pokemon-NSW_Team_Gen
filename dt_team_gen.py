#!usr/bin/python3

import numpy as np
import pandas as pd
import itertools as itt

# input: WRM(Weakness Resistance Matrix), IT(Input Types)
def create_WL(wrm, it):
	# weakness list (elements are the types super-effective against IT)
	wl = []
	for x in range(len(wrm)):
		# x versus types in it
		xvit = wrm[x][it[0]]*wrm[x][it[1]]
		if xvit >= 2:
			wl.append(x)
	return wl

# input: 1st WL, 2nd WL
# wl: Weakness List
def compare_WL(wl1, wl2):
	# the intersection of wl1 and wl2
	intersection = list(set(wl1)&set(wl2))
	# returns True if intersection is empty, False otherwise
	return (len(intersection) == 0)

# input: type tuple list of size 6x2
def compare_all_WL(ttl):
	return compare_WL(ttl[0][1],ttl[1][1]) and compare_WL(ttl[0][1],ttl[2][1]) and compare_WL(ttl[0][1],ttl[3][1]) and compare_WL(ttl[0][1],ttl[4][1]) and compare_WL(ttl[1][1],ttl[2][1]) and compare_WL(ttl[1][1],ttl[3][1]) and compare_WL(ttl[1][1],ttl[4][1]) and compare_WL(ttl[2][1],ttl[3][1]) and compare_WL(ttl[2][1],ttl[4][1]) and compare_WL(ttl[3][1],ttl[4][1])

# input: result from populate_FML
def check_duplicate_type(result):
	for x in itt.combinations(result,2):
		x_intersection = list(set(x[0][0])&set(x[1][0]))
		if (len(x_intersection) > 0):
			return 0
	return 1 

# input:potential dual-types, final members list
def populate_FML(pdt, fml):
	for result in itt.combinations(pdt,5):
		# print(list(result))
		if check_duplicate_type(list(result)) and compare_all_WL(result):
			fml.append(list(result))

def main():
	# Text to number
	TTN = {"normal":0, "fighting":1, "flying":2, "poison":3, "ground":4, "rock":5, "bug":6, "ghost":7, "steel":8, "fire":9, "water":10, "grass":11, "electric":12, "psychic":13, "ice":14, "dragon":15, "dark":16, "fairy":17}
	# Number to text
	NTT = ["normal","fighting","flying","poison","ground","rock","bug","ghost","steel","fire","water","grass","electric","psychic","ice","dragon","dark","fairy"]

	# non-existent dual-types
	NEDT = [[0,3],[0,5],[0,6],[0,7],[0,8],[0,14],[1,4],[1,12],[3,8],[3,13],[3,14],[4,17],[5,7],[6,15],[6,16]]

	# weakness resistance matrix
	WRM = pd.read_csv("WRM.csv").to_numpy()
				
	f1 = open("dt_input.txt","r")

	# Input types
	IT = [TTN[i] for i in f1.read().strip().lower().split(",")]

	f1.close()
	
	# potential dual-types
	PDT = []

	# final members list
	FML = []

	# input types weakness list
	ITWL = create_WL(WRM, IT)

	for result in itt.combinations([x for x in range(18)],2):

		intersection = list(set(IT)&set(list(result)))
		if (list(result) not in NEDT and len(intersection) == 0):
			# temporary weakness list
			TWL = create_WL(WRM,result)
			if compare_WL(ITWL,TWL):
				PDT.append([list(result),TWL])

	populate_FML(PDT, FML)

	f2 = open("dt_output.txt","w")

	for x in IT:
		f2.write(NTT[x]+" ")
	f2.write("\n")

	for w in FML:
		FINAL = [str([[NTT[z] for z in y] for y in x])+"\n" for x in w]
		f2.writelines(FINAL)
		f2.write("\n")

	f2.close()

main()