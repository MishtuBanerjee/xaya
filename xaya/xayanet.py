#!/usr/bin/env python
"""
BeginDate:20071001
CurrentRevisionDate:20071001
Development Version : net 001
Release Version: pre-release


Author(s): Mishtu Banerjee
Contact: mishtu@harmeny.com

Copyright: The Authors
License: Distributed under MIT License
    [http://opensource.org/licenses/mit-license.html]
    
Environment: Programmed and tested under Python 2.3.3 on Windows 2000.
    Database Access: Psycopg and Postgres 7.4
    
Dependencies:
    Python Interpreter and base libraries.
    Psycopg [website]
    Postgres [website] test X
    


==============================================
XAYAnet_001 A Toolkit for Exploring Networks
==============================================


XAYAcore is a Pythonic implementation of the Graph Abstraction Logic (GAL)
design principles. GAL relationally models information as graphs (an old idea
originating in modern logic) as a "little language" that can embedded
or embellished. It provides a basis for modelling and querying data from
complex systems. Data---> Information--> Knowledge (but wisdom is golden).

GAL was inspired by Robert Ulanowicz's ecological network theory of Ascendency,
Stan Salthe's developmental theory of Hierarchical Systems,
and Charles Peirce's Existential Graphs (a visual method of doing logic).
Hopefully beautiful ideas can lead to pragmatic working code ;-} ...

Xayacore goes frominstances to ontologies,and points inbetween.
One graph to rule them all! And some common sense to bind them ...

Send bugs, fixes, suggestions to mishtu@harmeny.com (Thanks). 



USAGE EXAMPLE: (see examples under individual functions)

ALGORITHMs:
    AlgorithmName -- Reference

CODE SOURCES:
    Guido Code. [webref]
    Graphlib Code
    Pydot Code
    Graphpath Code
    Python Cookbook
    Djikstra's
    Algorithms in Python

REFERENCES:
    Ascendency book.
    Salthe Hierarchy Book.
    Peirce Book (Reasoning and the Logic of Things)
    Graph Algorithms Reference
    Information Flow Book
    Foundations of Logic.
    Tools for Thought book


"""

# KNOWN BUGS
# None Known at this point

# UNITTESTS
# Unittests are below fn/obj being tested

# DESIGN CONTRACTS
# Design Contract for each fn/obj is right after docstring

#DOCTESTS
# Used sparingly where they illustrate code above and beyond unittest

import types
#from math import sqrt
import math
import xayacore
import xayastats
import pprint
import random
import copy
import sets



# To allow the code to use built-in set fns in Python 2.4 or the sets module in Python 2.3
try :
    set
except NameError:
    from sets import Set as set

def xayanetVersion():
    return "Current version is xayanet_001 (development branch), updated October 1, 2007"

# ---------- Utility Functions ----------
# These functions handle basic 'data munging' tasks, calculate probablities,
# allow for sampling and audit of data
# Basic math tricks for sums and series



def readNetwork(filepath = ""):
    """
    
            
    """
    
    
 


def writeNetwork(graph = {}, filepath = "defaultFilePath"):
    """ Inverse of readGraph. Stores a XAYA format dictGraph as a text file"""
    transList = transGraphToList(graph)
    fileObject = open(filepath, 'a+')
    fileObject.writelines(transList)
    fileObject.flush()
    return fileObject


def shelveNetwork(graph = {},filepath = "defaultFilePath"):
    """ Stores via the Graph at the filepath location e.g '/apath/file.xay'
    Preconditions: Takes a graph
    Postconditions: Returns a shelf object with stored graph
    
    Usage:
    >>> agraph = {'Key1': ['Value1', 'Value2'], 'Key2':['Value3',4]}
    >>> shelveGraph(agraph,'storeagraph')
    {'Key2': ['Value3', 4], 'Key1': ['Value1', 'Value2']}
    >>>

    Algorithms (see pseudocode below)
    #Open a shelfObject
    #read graph into shelfObject; deal with case of emptygraph via get fn
    #return shelfObject

    """

#DATASETS FOR FIND COMPONENTS
anetwork = {'a': [1,2,3], 'b' : [4,5,6], 1 : ['d', 'e', 'f']}    

nothernetwork = {'a': [1,2,3], 'b' : [4,5,6], 1 : ['d', 'e', 'f'], 4: ['e', 'f', 'g'],
              'x': [9, 10,11], 11: [12, 13, 14]}


loopnetwork = {'a': [1,2,3], 'b' : [4,5,6], 1 : ['d', 'e', 'f'], 4: ['e', 'f', 'g'],
            12: [13], 13: [12]} 

#DATASETS FOR MUTUAL INFORMATION
fullyconnet = {'a':['a','b','c'],
               'b': ['a', 'b', 'c'],
               'c': ['a','b','c']}
noselfcon = {'a':['b','c'],
               'b': ['a', 'c'],
               'c': ['a','b']}
cycle3 = {'a':['b'],
         'b':['c'],
         'c':['a']}


cycle4 = {'a':['b'],
         'b':['c'],
         'c':['d'],
          'd':['a']}

tree = {'a': ['b','c'],
        'b': ['d', 'e'],
        'c': ['f', 'g'],
        'd': ['h', 'i'],
        'e': ['j', 'k']}

def findComponents (graph = {}):
    """
    Given a directed graph (network) findComponents returns a list of isolated
    "Islands in the Network" or components. Within an island, there are paths
    to nodes. Across islands, there is not direct path.
    General Algorithm:
    
    1. Define the keyset (the parent nodes in a set of directed arcs)
    2. Assign each parent node and its direct children (arcs) to a new component
    3. Iterate through the node-set and combine parent nodes that have paths, including their child arcs
        (These are the candidate components)
    4. Remove candidate components that are subsets of each other.
    5. Create final components from the remaining candidate components
        (and do a check on the results of loops -- note this may be a bug in the path-finding algorithm)
    6. Return the final list of components 
    """
    
    # Define the keyset
    keys = graph.keys()
    keys2 = copy.deepcopy(keys)
    
    # For each key,  assign arcs to a new component.
    compgraph = {}
    compkey = 0
    for key in keys:
        compkey = compkey +1
        compgraph[compkey] = [key] + graph[key]
        
        # Iterate through keys, and combine pairs of keys with a path between them
        # These are the 'candidate' components
        for dkey in keys2:
            if key <> dkey:
                if xayacore.findAllPaths(graph, key, dkey) <> {}:
                    compgraph[compkey] =  [key] + graph[key]  + graph[dkey]
                    keys2.remove(key) # remove the key that has been combined

    # Remove candidate components that are simply subsets of each other
    compkeys = compgraph.keys()
    compkeys2 = copy.deepcopy(compkeys)
    for key in compkeys:
        for nextkey in compkeys:
            if key <> nextkey:
                set1 = set(compgraph[key])
                set2 = set(compgraph[nextkey])
                if set1.difference(set2) == set([]) and set2.difference(set1) <> set([]):
                    compkeys2.remove(key)
                    
                            
    # Create Final components                        
    finalcomp = {}
    finalcompkey = 0
    for key in compkeys2:
        # Check on and remove the output from loops -- same element is repeated so list <> set cardinality
        if len(compgraph[key]) == len(set(compgraph[key])): 
            finalcompkey = finalcompkey + 1
            finalcomp[finalcompkey] = compgraph[key]
   

    
    return  finalcomp

def countArcs(graph = {}):
    
    # Calculate Number of Arcs in graph
    arcounter = 0
    for key in graph:
        arcounter = arcounter + len(graph[key])
    return arcounter
    

def calcMI(graph= {}):
    '''Given a xayaformat graph -- calculates the mutal information of the
    adjacency matrix of connections (i.e. does not assume flow values)
    '''
    sources = graph
    destinations = xayacore.reverseGraph(sources)
    # Calculate Number of Arcs in graph
    arcounter = 0
    for key in sources:
        arcounter = arcounter + len(sources[key])
    pSourceDest = 1/float(arcounter)
    sumMI = 0
    for key in sources:
        # calc P(Source/Destination)
        for arc in sources[key]:
            # calc P(Source)
            pSource = len(sources[key])/float(arcounter)
            # calc P (Destination)
            pDest = len(destinations[arc])/float(arcounter)
            # calc MI
            quotient = pSourceDest/(pSource * pDest)
            #Test Code: print pSourceDest, pSource, pDest, quotient
            mi = pSourceDest * math.log(quotient,2)
            sumMI = sumMI + mi
                        
    return sumMI

def createModelBipGraph(network = {}):
    '''
    Given a network, creates a bipartite graph with the same number of arcs,
    and the same degree distribution on keys
    '''
    bipgraph = {}
    arcs = countArcs(network)
    counter = arcs*10 #just to make sure keys start at much higher numbers
    for key in network:
        counter = counter+1
        samples = len(network[key])
        arclist = xayastats.samplePopulationsNoR(samples,arcs)
        bipgraph[counter] = arclist
    return bipgraph
        


def test():
    if 1 == 2:
        print 'false'
    else: print 'true'


def createRandomDirectedNetwork(nodes=0, edges=0):
    '''Given a number of nodes and edges, generate a random directed graph
    in XAYA format, where each edge is randomly generated. Arcs from a node,
    back into that node are disallowed in the current version. 
    Last modified, Sept, 29, 2009. 
    '''
    #Create an empty network data structure
    network = {}
    #If either nodes or edges are 0/negative, return an empty graph
    if (nodes <=0) or (edges <= 0):
        return network
    # Check that edges < nodes * (nodes-1) -- i.e. a complete graph minus self-arcs
    if edges >  nodes * (nodes - 1):
        return network
    
    #Use while loop to determine when sufficient edges produced
    while countNetworkEdges(network) < edges:
    
        #Generate a node value
        nodevalue = xayastats.diceroll(1,nodes)
        #Generate an Edge value
        edgevalue = xayastats.diceroll(1,nodes)
        #Check for self-loops. If self loop return to top of While 
        if nodevalue != edgevalue:
            #If node does not already exist, add it and value
            if not network.has_key(nodevalue):
                network[nodevalue] = [edgevalue]
            else:
                #Check if value already in an arc, and if not, add it. 
                if edgevalue not in network[nodevalue]:
                    network[nodevalue].append(edgevalue)
    #reversednetwork = xayacore.reverseGraph(network)-- not working as expected
    #undirectednetwork = xayacore.unionGraphs(network, reversednetwork) --nwaexpcted
    return network


def countNetworkEdges(network):
    noedges = 0
    for value in network.values():
        noedges = noedges + len(value)
    return noedges

def runVirusSimulator(network={}, immuneprob=1, viralprob=1, precision=10, iterations=25, itertables=0):
    '''Virus Simulation consists of:
    1. Initializing a state table for the network
    2. Initializing an initial point of infection on the statetable
    3. Running the simulation
       3a Immune Phase
       3b Viral Immune Phase
       3c Viral virulent phase
       itertables is a key, which if set to <> returns all intermediate tables, if set to 0, returns only the final table
    '''
    # Initialize
    initial_statetable = simInitialNodestate(network)
    initialvirus_statetable = simInitialVirus(initial_statetable)
    # Run simulation for a number of iterations
    iterationlist = range(iterations)
    updatedstatetable = initialvirus_statetable
    interimtables = {}
    interimtables[0] = updatedstatetable
    # Run simulation for X iterations, updateing statetables
    for iteration in iterationlist:
        ##print 'iteration is', iteration
        ##print 
        ##print updatedstatetable
        ##print
        # Immune Phase
        immune1statetable = simImmunePhase(network, updatedstatetable)
        # Virus Immeune Phase
        immune2statetable = simVirusImmunePhase(network,immune1statetable,immuneprob,precision)
        # Virus Virulent Phase
        viralstatetable = simVirusViralPhase(network,immune2statetable,viralprob,precision)
        updatedstatetable = viralstatetable
        interimtables[iteration + 1] = updatedstatetable
    if itertables != 0:
        return interimtables
    else: return updatedstatetable
        
def createStatetableDataset(statetable = {}, label = ''):
    '''
    Given a statetable, creates a XAYA format dataset with the following columns:
    Name, Node, State
    '''
    newdataset = {}
    variables = {'Label':[0],
                 'Node': [1],
                 'State': [2]}
    data = {}
    data[0] = ['Label', 'Node', 'State']
    autonumberkey = 0
    for node in statetable:
        autonumberkey = autonumberkey + 1
        data[autonumberkey] = [label, node, statetable[node][0]]
    newdataset['VARIABLES'] = variables
    newdataset['DATA'] = data
    return newdataset

def createVirusSimDataset(statetables={}, name = ''):
    newdataset = {}
    variables = { 'Name':[0],
                  'Iteration':[1],
                  'Node': [2],
                  'State': [3]
                  }
    data = {}
    data[0]= ['Name', 'Iteration', 'Node', 'State']
    autonumberkey = 0
    for iteration in statetables:
        
        for node in statetables[iteration]:
            autonumberkey = autonumberkey + 1
            data[autonumberkey] = [name, iteration, node, statetables[iteration][node][0]]
    newdataset['VARIABLES'] = variables
    newdataset['DATA']=data
    return newdataset


def summarystatVirusSimDataset(simdataset={}):
    '''
    Summarizes each iteration for a VirusSimDataset
    
    Algorithm Outline:
    1. Filter the Dataset by Iteration
    2. Calculate Histogram for each Iteration
    3. Add histogram data to a new dataset
    

    
    '''
    # Set Up the New Summary Stat Dataset 
    newdataset = {}
    variables = { 'Name': [0],
                  'Iteration': [1],
                  'ViralNodes': [2],
                  'NeutralNodes': [3],
                  'ImmuneNodes': [4]
                  }
    data = {}
    data[0] = ['Name', 'Iteration', 'ViralNodes', 'NeutralNodes', 'ImmuneNodes']
    # Identify how many iterations are in the dataset
    iterationslist = list(set(xayastats.getIntegerslist(dataGraph=simdataset['DATA'], varGraph=simdataset['VARIABLES'], variable='Iteration')))
    #filter the dataset by iteration
    autonumberkey = 0
    for iteration in iterationslist:
        autonumberkey = autonumberkey + 1

        # Extract the data for that iteration, the name, and the number of viral, neutral and immune nodes         
        filtereddata = xayastats.filterDataset(dataset=simdataset, filterVar='Iteration', filterValues=[iteration])
        name = list(set(xayastats.getDatalist(dataGraph=filtereddata['DATA'], varGraph=filtereddata['VARIABLES'], variable='Name')))[0]
        #Calculate the histogram for the statetable
        histogram = xayastats.getHistograph(dataset=filtereddata, variable='State')
        # Extract number of viral nodes (-1), neutral nodes (0), and immune nodes (1).
        if histogram.has_key(-1):
            infectednodes = histogram[-1][0]
        else: infectednodes = 0
        if histogram.has_key(0):
            neutralnodes = histogram[0][0]
        else: neutralnodes = 0
        if histogram.has_key(1):
            immunenodes = histogram[1][0]
        else: immunenodes = 0
        # Build up dataset iteration by iteration
        data[autonumberkey] = [name, iteration, infectednodes, neutralnodes, immunenodes]
        newdataset['VARIABLES'] = variables
        newdataset['DATA']=data
    return newdataset
                          
                  

def simImmunePhase(network={}, statetable={}):
    '''For all nodes in state "i"(mmune), immune response at
    probability  immune response at probability 1.
    All child nodes in "u"(ninfected) state change to "i"(mmune)
    state. States: "i"(mmune)=1, "v"(irus)=-1, "u"(ninfected)=0. 
    '''
    # Check that network or statetable not empty.If empty return current statetable
    if len(network.keys()) < 1 or len(statetable.keys()) < 1:
        return statetable
    newstatetable = copy.deepcopy(statetable)
    parentnodelist = copy.deepcopy(network.keys())
    for node in parentnodelist:
        if statetable[node]==[1]:
            for arc in network[node]:
                if statetable[arc] == [0]:
                    newstatetable[arc] = [1]
    return newstatetable


def simVirusImmunePhase(network={}, statetable={}, prob=1, precision=10):
    '''For all nodes in state "v"(iral), immune response at
    probability Q.
    States: "i"(mmune)=1, "v"(irus)=-1, "u"(ninfected)=0.
    '''
    # test that proability is below 1:
    if prob < 0 or prob >1: return {}
    # hinge is the number required for dicebool -- <= hinge returns a 1, else 0
    hinge = int(prob*precision)
    # test you do not have an empty network or statetable
    if len(network.keys()) < 1 or len(statetable.keys()) < 1:
        return statetable
    newstatetable = copy.deepcopy(statetable)
    parentnodelist = copy.deepcopy(network.keys())
    # for parent node
    for node in parentnodelist:
        # if its statetable is in viral state
        if statetable[node]==[-1]:
            for arc in network[node]:
                # and the child node on the arc is in uninfected state
                if statetable[arc] == [0]:
                    # Roll the dice, and return 1 if the roll is below the hinge
                    randvalue = xayastats.dicebool(1,precision,hinge)
                    if randvalue == 1:
                        # then update the state table
                        newstatetable[arc] = [1]
    return newstatetable



def simVirusViralPhase(network={}, statetable={}, prob=1, precision=10):
    '''For all nodes in state "v"(iral), virulence response at
    probability p. 
    States: "i"(mmune)=1, "v"(irus)=-1, "u"(ninfected)=0
    '''
    # test that proability is below 1:
    if prob < 0 or prob >1: return {}
    # hinge is the number required for dicebool -- <= hinge returns a 1, else 0
    hinge = int(prob*precision)
    # test you do not have an empty network or statetable
    if len(network.keys()) < 1 or len(statetable.keys()) < 1:
        return statetable
    newstatetable = copy.deepcopy(statetable)
    parentnodelist = copy.deepcopy(network.keys())
    # for parent node
    for node in parentnodelist:
        # if its statetable is in viral state
        if statetable[node]==[-1]:
            for arc in network[node]:
                # and the child node on the arc is in uninfected state
                if statetable[arc] == [0]:
                    # Roll the dice, and return 1 if the roll is below the hinge
                    randvalue = xayastats.dicebool(1,precision,hinge)
                    if randvalue == 1:
                        # then update the state table, to virus state
                        newstatetable[arc] = [-1]
    return newstatetable

def simInitialNodestate(network):
    '''Given a network in Xaya format, generates an inital
    nodestate dictionary.    
    '''
    # Generate sets of parent and child nodes
    parentnodeset = sets.Set(network.keys())
    childnodelist = []
    for arclist in network.values():
        for node in arclist:
            childnodelist.append(node)
    childnodeset = sets.Set(childnodelist)
    # Union Parent and Childe Nodes
    allnodes = parentnodeset.union(childnodeset)
    # Generate Initial Node state table -- set to 0 'uninfected'
    statetable = {}
    for node in sorted(list(allnodes)): # sorted and list functions create stable with ascending integers
        statetable[node] = [0] # Current States: 0 = uninfected, -1= infected, 1 = immune
    return statetable
    
    

def simInitialVirus(statetable):
    ''' Given an statetable, randomly selects an initial node to be
    put into the 'viral' state
    '''
    # Since we're dynamically updating a dictionary, deep copy it first. 
    newstatetable = copy.deepcopy(statetable)
    # If statetable has nodes, selext a ranom node
    if len(statetable.keys()) > 0:
           updatenode = random.choice(statetable.keys())
           newstatetable[updatenode] = [-1]
           return newstatetable
    # Otherwise -- just return the original (empty) statetable
    else: return statetable

def NOTWORKINGcreateRandomUndirectedNetwork(nodes=0, edges=0):
    '''Given a number of nodes and edges, generate a random undirected graph
    (as pairs of edges in a directed graph) where each edge is randomly generated,
    sampling is without replacement -- so no edge is generated twice. 
    '''
    #Create an empty network data structure
    network = {}
    #Set EdgeCounter to 0
    edgecounter = 0
    # Start Node and Edge Generation loop
    while edgecounter < edges:
        #Generate a node value
        nodevalue = xayastats.diceroll(1,nodes)
        #Generate an Edge value
        edgevalue = xayastats.diceroll(1,nodes)
        # Check if network has node and edge values already -- bidirectional
        # Check forward order
        alreadyin = 0
        if network.has_key(nodevalue):
            if edgevalue in network[nodevalue]:
                alreadyin = 1
        # Check Reverse Order
        if network.has_key(edgevalue):
            if nodevalue in network[edgevalue]:
                alreadyin = 1
        # If arc does not exist already
        if alreadyin != 1:
            #If node does not already exist, add it and value and iterate counter
            if not network.has_key(nodevalue):
                network[nodevalue] = [edgevalue]
                edgecounter = edgecounter + 1
            # Otherwise add the value and iterate counter
            else: network[nodevalue].append(edgevalue)
            edgecounter = edgecounter + 1
        
    else: return network    
 

# REVISION HISTORY
# Revised XXX by YYY
