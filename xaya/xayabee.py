#!/usr/bin/env python
"""
xayabee: a little dose of bee genetics ...

BeginDate:2012
CurrentRevisionDate:20150324
Development Version : core 001
Release Version: pre-release

Author(s): Mishtu Banerjee, Robin Owens
Contact: mishtu_banerjee@shaw.ca

Copyright: 2012-2015, The Authors
License: Distributed under MIT License
    [http://opensource.org/licenses/mit-license.html]
    
Original Environment: Programmed and tested under Python 2.7.X
 
Dependencies:
    Python Interpreter and base libraries.
    xaya: xayacore, xaystats

"""
import xayastats

def genHaploid(numberofalleles= 0):
	"""
	Given a number of sex alleles, randomly generate a haploid genotype.
	"""
	#Set internal variable from parameters
	alleles = numberofalleles
	# Randomly generate haploid
	haploid = xayastats.diceroll(1, alleles)
	return (haploid) # return haploid as a 1 item tuple


def genDiploid(numberofalleles=0):
	"""
	 
	"""
	alleles = numberofalleles
	diploid = (xayastats.diceroll(1,alleles), xayastats.diceroll(1,alleles))
	return diploid # return dipoid as a two item tuple

def createPop(numberalleles= 0, dippopsize=0, happopsize=0):
	"""
	Build haploid and diploic population given alleles, number of diploids, number haploids
	"""
	# Set internal variables from parameters
	alleles = numberalleles
	diploids = dippopsize
	haploids = happopsize
	# Build a list of haploids
	haploidcounter = range(haploids)
	haploidslist = []
	for bee in haploidcounter:
		haploidslist.append(genHaploid(alleles))
	# Build a list of diploids
	diploidcounter = range(diploids)
	diploidlist = []
	for beecouple in diploidcounter:
		diploidlist.append(genDiploid(alleles))
	return [haploidslist, diploidlist]
	# Next we must build up a dictonary where keys are tuples and
	# the values are counts.
	# Later can make the values more complicated as lists, dicts.
	# Give Robin the choice -- and ask him how he likes it. 
	# if lists -- can have multiple properties
	# if values -- can have named properties:"COUNT"; MUTATION RATE

def summarizePop(poplist=[]):
	"""
	Creates a summary table of the bee population
	"""
	mypop=poplist
	myhaploids=poplist[0]
	mydiploids=poplist[1]
	myhaptable = xayastats.histograph(myhaploids)
	mydiptable=xayastats.histograph(mydiploids)
	return [myhaptable, mydiptable]

def findHomozygotes(diptable={}):
	"""
	Given a summary table of diploids, finds those 
	which are homozygous
	"""
	mydiptable=diptable
	homozygouslist=[]
	mydipkeys=mydiptable.keys()
	for key in mydipkeys:
		if key[0]==key[1]:
			homozygouslist.append(key)

	homozygtable = {}
	for key in homozygouslist:
		homozygtable[key] = mydiptable[key]
	return homozygtable	

def countPopulation(poptable):
	"""
	Counts all indivuals in a population; can be applied to 
	a diploid, haploid, or homzygotes table
	"""
	mypoptable = poptable
	vals = mypoptable.values()
	vals2 = []
	for item in vals:
		vals2.append(item[0])
	popsum = sum(vals2)
	return popsum

# Create a function checkforHomozygotes
# Get population as a dictionary where keys are alleles and values are counts