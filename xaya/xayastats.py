#!/usr/bin/env python
"""
BeginDate:20050824
CurrentRevisionDate:20091021
Development Version : xayastats 001
Release Version: pre-release
Filename: xayastats.py
Filedescription: xayastats.py contains basic statistics and exploratory data analysis
primitives. 

Author(s): Mishtu Banerjee
Contact: mishtu_banerjee@shaw.ca

Copyright: The Authors
License: Distributed under MIT License
    [http://opensource.org/licenses/mit-license.html]
    
Environment: Programmed and tested under Python 2.3.3 on Windows 2000.

    
Dependencies:
    Python Interpreter and base libraries.
    xayacore
    


==============================================
XAYAstats_001 A Toolkit for Model Driven Data Analysis
==============================================


XAYAstats adds basic statistics capabilities to the data processing
capabilities of XAYAcore.

XAYAstats adds control functions that call  on the lower level genStats functions
that operate on lists, so they can work with XAYA format data sets.

This module does not use Numeric -- to limit dependencies     It simply
uses the Python built in fns. It uses a functional style, starting with
simple stat functions, and building more complex stats from them like
in the language R or in MatLab.

Send bugs, fixes, suggestions to mishtu@harmeny.com (Thanks)




Description of Functionality of XAYAstats 

    The basic unit in XAYAstats is a 'Dataset'..
    While primitives in XAYAstats operate on lists, the "control" functions
    in XAYAstats operate on Datasets (from which they extract and compose lists
    as needed. genStats assumes it's input is a "dataset". A dataset has
    3 core components: 'VARIABLES', 'DATA', 'VARTYPES'
    There are several optional components: GROUPS, SORTS, VARDICTIONARY.
    

    Each of these components is represented as a XAYAcore format graph.
    A Dataset is a collection of these graphs, held in a Python dictionary. 

    a dataset is a dictionary that contains several  XAYA format graphs as
    its values:('DATA' and 'VARIABLES' are required, others are optional)

            'DATA': keys are "autonumbers" representing a line of data, and
                values are the tuple of data
            
            'VARIABLES': keys are the variable names, and values are the
                index position of that variable in the tuples in 'DATA'.
            
            'VARTYPES'. keys are the variable names and values are the data type.
                There are five data types:
                    'INTEGER' -- a whole number
                    'NUMERICAL' -- any number with a decimal
                    'CNUMBER'  -- a complex number -- not currently supported
                    'CATEGORICAL' -- a series of labels
                    'TEXT' -- free text.

    'VARTYPES' in this case are a set of data-analysis centric categories.
    Additional types would exist in a database centric,
    or programming language centric characterization of data types. 

    'DATA' and 'VARIABLES' are mandatory keys, 'VARTYPES' is optional.
    In the abscence of explicit type information, data
    is cast based on a series of tests (see the function testTypes)





Example of the structure of a XAYAstats dataset

    dataset = {'VARIABLES' : {'Var1' : [0],
                                             'Var2': [1],
                                             'Var3': [ 2] }
                        'DATA' : {1 : [1,2,3],
                                        2 : [4, 5, 6]}
                        'TYPES' : {'Var1' : 'CATEGORICAL',
                                          'Var2' : 'NUMERICAL',
                                          'Var3' : 'INTEGER'}
                        }
                                             





Description of Functionality of XAYAstats data analysis primitives:

    These 'primitives' for data analysis generate
    basic statistics. They can be called individually.
    They can be combined. If you have a module to access
    dbs and files and represent the data as lists, then
    this package can calculate all basic stats on those
    lists.

    Probably 80 % of the stats people calculate are these
    very simple stats.

    UNIVARIATE STATISTICAL FUNCTIONS:

    getStats -- Calculates univariate statistics for a dataset based on
        a user-supplied list of selected statistics. Returns a XAYAstats
        format dataset.

    getSummaryStats -- Calculates a pre-defined list of summary statistics
        for a dataset. Returns results in a dictionary format that is easy to
        display with the pretty-print function. 
    
    callStats -- Calls the individual statistics functions and returns a
        XAYAstats format dataset. Is itself called by getStats. Can call
        any of the stats primitives in the list below from minstat to cvstat.
        Can not call summarystat function.

    getHistograph -- returns a histograph from a dataset. See the
        histograph function for more details. 

    minstat -- minimum
    maxstat -- maximum
    rangestat -- absolute range
    sumstat -- sum of values
    sumsqstat -- sum of squares of values
    meanstat -- mean
    medianstat -- median
    varstat -- variance of a sample
    sdstat -- standard deviation of a sample
    cvstat -- coefficient of variation -- biologists like
              it, for reasons that were never clear to me
              
    summarystat -- provides dictionary of basic summary
                statistics for a sample (not in XAYAstats format,
                but easy to view with pretty-print function)
                

    STATS VARIABLE TRANSFORMATIONS:

    dlist -- list of deviations from mean value
    zlist -- list of z scores -- deviation from mean value
             divided by standard deviation
    rlist -- dev from min divided by range -- list between 0 and 1

    DISTRIBUTIONS:

    histograph -- Counts occurances of each unique item in a list and
        represents the results as a XAYAcore format graph. 





Description of functionality of XAYAstats dataset handling functions:


    Functions that operate on XAYAstats format Datasets

        getDataset : Creates a XAYAstats format dataset (calling readFile and getData)
    
        viewData : Allows one to view the Data components of a Dataset
    
        viewVariables: Allows one to view the Variables component of a Dataset
    
        saveData: Saves the Data component of a Dataset to a XAYAcore style text file.
    
        saveVAriable: Saves the Variable component of a Dataset to a XAYAcore
            style text file.     
    
        getDatalist: Extracts a Variable from a Dataset -- does not cast to
            a particular variable type.
            (can be treated as either CATEGORICAL or TEXT)

         getNumberslist: Extracts a Variable as a list of numbers from a
            Dataset via castDatalistToNumerical

        getIntegerslist: Extracts a Variable as a list of integers.
        

    Functions that operate on a File        
    
         readFile : Reads csv file into dictionary keyed to file line numbers.
            Headings at line 0.
    
        getData: Cleans up dictionary, strips off extra spaces,
            turns the dictionary value into a list of numbers.
    
        getVariables: From csv file header, creates a graph where the
            column name is the key, and the column index is the value.
            This dictionary extracts lists of values by column name.


    Functions that operate on Lists            

        castDatalistToNumerical: Converts a Datalist to floating point numbers.
    
        castDatalistToInteger: Converts a Datalist to integers.
    
        getNumberslist: Extracts a Variable as a list of numbers from a
            Dataset via castDatalistToNumerical
    
        Functions that operate on individual data items        
    
        testTypes -- Tests whether an item is INTEGER, NUMERICAL, CATEGORICAL,
            or TEXT       
    




Description of functionality of Utility Functions:

    These functions are designed to "round out" XAYAstats by
    providing it with additional data manipulation ('data munging' aka
    'data crunching') abilities to further organize, clean-up, and transform
    data. Additionally there is support for basic sampling procedures, and
    basic probability calculations will be added soon.

    Sampling and audit Functions:    

        auditDataset -- Produces an audit sample for a dataset, using a
            probability for inclusion based on the number of audit samples
            requested. The function will return approximately the number
            of samples requested.
    
        auditData -- Called by auditDataset. Handles the sampling process.
            Can be used to sample any XAYAcore format graph.

        sampleDataset -- Samples a dataset with or without replacement.
            This function can be used for various monte-carlo like simulations
            based on repeated sampling from a dataset.

        samplePopulationR -- Called by sampleDataset if replacement = 'Y'.

        samplePopulationNoR -- Called by sampleDataset if replacement = 'N'

 
    Probability Calculators

        diceroll -- approximates rolling a number of dice, each of which can
            have an aribtrary number of sides.  For example, diceroll(5, 6)
            would be 5 rolls of a 6 sided dice
    

    Data munging Functions (aka data crunching ....)

        sortlist -- a Python 2.3 version of the "sorted" feature in Python 2.4.
            Sorts a copy of a list, and leaves the original list unchanged. 

        
    





SOURCES:
Sources for specific statistics are cited in the docstring for the statistic.
The rest of the statistics, just follow  from their standard definitions.


USAGE EXAMPLEs:
(see examples under individual functions -- not implemented currently)



REFERENCES:
  
# KNOWN BUGS
# None Known at this point

# UNITTESTS
# Unittests are in the file test_xayastats

# DESIGN CONTRACTS
# Design Contract for each fn/obj are currently described in comments/docstring

#DOCTESTS
# Used sparingly where they illustrate code above and beyond unittest

"""

import types
from math import sqrt
import xayacore
import pprint
import random

# To allow the code to use built-in set fns in Python 2.4 or the sets module in Python 2.3
try :
    set
except NameError:
    from sets import Set as set

def xayastatsVersion():
    return "Current version is xayastats_001 (development branch), updated September 6, 2005"

# ---------- Utility Functions ----------
# These functions handle basic 'data munging' tasks, calculate probablities,
# allow for sampling and audit of data
# Basic math tricks for sums and series


def listDatasets(objects = dir()):
    """
     Utility function to identify currently loaded datasets.
    Function should be called with default parameters,
    ie as 'listDatasets()'
    """
    datasetlist = []
    for item in objects:
        try:
            if eval(item + '.' + 'has_key("DATA")') == True:
                datasetlist.append(item)
        except AttributeError:
            pass
    return datasetlist




def auditDataset (auditsamples=1, dataset ={}, randseed=12345213):
    """
    Wraps auditData function to operate on a XAYAstats format dataset.
    Type help(auditdata) for more information on the underlying function
        
    """
    data = dataset['DATA']
    auditsample = {}
    auditsample['DATA'] = auditData(auditsamples, data, randseed)
    auditsample['VARIABLES'] = dataset['VARIABLES']
    return auditsample

def auditData(auditsamples = 1, data = {}, randseed = 12345213 ):
	"""
	Samples a DATA graph based on a probability of inclusion
	which is the ratio auditsamples/len(data). So, one recieves
	approximately 	the number of samples selected. From Data Crunching
	pg 170. This function uses a fixed seed, so it's results
	for a particular input are repeatable. The default seed is
	taken from the example in Data Crunching. 
	
	"""
	auditdata = {}
	random.seed(randseed)
	if (not data) or (len(data) <= auditsamples):
		auditdata = data
		return auditdata
	else:
		prob = float(auditsamples)/len(data)
		keys = data.keys()
		keys.remove(0)
		for key in keys:
			if random.random() < prob:
				auditdata[key] = data[key]
				auditdata[0] = data[0]
		return auditdata
	
	

def samplePopulationR(samples, population):
	"""
	Samples a population with replacement
	The same population member can be sampled
	more than one time
	In this function we are imagining s rolls of a
	single dice whose number of sides is equal
	to the population size. As population approaches
	infinity, the dice becomes round ... but you'll
	be dead before it happens.
	
	"""
	samplesList = [ ]
	for sample in range(samples):
		randomsample = diceroll(1,population)
		samplesList.append(randomsample)
	return samplesList

def samplePopulationsNoR(samples, population):
	"""
	Samples a population without replacement.
	If a population member is drawn once, it can not
	be drawn again. 

	"""
	maxsamples = samples
	initialsamples = 0
	samplesList = [ ]
	while (len(samplesList) < maxsamples) :
		if len(samplesList) == population: break 
		thissample = diceroll(1,population)
		if thissample not in samplesList:
			samplesList.append(thissample)
	return samplesList



def diceroll (dice, sides):
    """
    Simulate rolling d dice of s sides each
    From Python Cookbook1st Edn pg 531
    See the Python Cookbook entry on this
    function for the non-standard use of 'reduce'
    for example diceroll(5, 6) would be 5 rolls
    of a 6 sided dice

    """
    def accumulate (x, y, s=sides):
        return x + random.randrange(s)
    return reduce(accumulate, range(dice+1) )+ dice

def dicebool (dice, sides, hinge):
    ''' Booleanizes the resuls of a diceroll, based on
    a hinge value. For example, if we wanted to have an
    item selected with probability 0.5, we could use a
    10 sided dice, and assign 1 to any case where the diceroll
    value is <= 5. If we wanted probability 0.9 we could again
    use a 10 sided dice, and set the hinge at 9. If we wanted to
    select something with probability 0.63, we could roll a 100 sided
    dice, and use a hinge of 0.63. So this is a way of selecting items
    with an arbitary probability. 
    '''
    roll = diceroll(dice, sides)
    # print roll
    if roll <= hinge:
        return 1
    else: return 0


def sortlist(iterable = [ ]):
    """
    A utility function that returns a sorted list, but recieves the
    original list unchanged: from The Python Cookbook 2nd Edn pg  192
    
    """
    alist = list(iterable)
    alist.sort()
    return alist


def sumIntegerSeries(start = 1, stop = 100, difference = 1):
    """
    This formula is taken from pg 78/79 of "The Art of the Infinite" by Robert and
    Ellen Kaplan. It's based on an ancient trick for summing a series of numbers
    without having to go through all the middle-work
    For example if start = 1, stop = 5, and difference = 3
        sumint = 1 + 4 + 7 + 13 = 35
    There's also the famous "schoolboy in class exercise": Sum 1 to 100
        start = 1, stop = 100, difference = 1
        sumint = 1 + 2 + 3 + 4 + .... + 100 = 5050
   
    """
    sumint = (stop * (2 * start + (stop - 1) * difference)/2)
    return sumint
              

# ---------- readDataSetsdsv Functions ----------
# These functions are read a csv file, and put it in a xayastats dataset form
# May need further modification to put in XAYA format. 

def getDataset(filepath = ""):
    """
    Reads a comma separated variables (csv) file and creates a dataset.
    A dataset has the following components: Variables, Data, Types, Groups, Sorts
    To call each componenet of a dataset, do the following.
    Say you have a dataset named: somedata
    somedata['VARIABLES'] accesses the variables in this dataset
    somedata['DATA'] accesses the rows of data in this dataet.
    
    """
    data = {}
    data['VARIABLES'] = getVariables(filepath)
    data['DATA'] = getData(filepath)
    return data


# Notes for version with type support added
#   def getDataset(filepath = "", varGraph = {}, typesGraph = {}):
#       """   Given a filepath, create a data table and a variables table   """
#    
 #      data = {}
 #       if varGraph == {}:
#             data['VARIABLES'] = getVariables(filepath)
 #      else:
 #           data['VARIABLES'] = varGraph
 #       if typesGraph == {}:
 #            data['VARTYPES'] = typesGraph
 #     else: data['VARTYPES'] = guessTypes
 #     data['DATA'] = getData(filepath)
 #    return data

def saveDataset(dataset = {}, filepath = "", append=0):
    """
    Reads a XAYA format dataset into a csv file where the first row contains
    the file headings and all other rows contain the data. Inverse of getDataset.
    Algorithm:
    1.  'DATA' component of dataset translated into a list of strings -- transList
    2. Write transList to a file object
    'append' keyword: 0 includes headings, not 0 is append mode and headings are not written

    

    
    """
    #  'DATA' component of dataset translated into a list of strings -- transList (see xayacore transGraphToList)
    transList = []
    # If append mode -- then skip line 0 -- the headings
    if append != 0:
        for key in dataset['DATA']:
            if key != 0:
                valueString =  " ".join([str(x) + ',' for x in dataset['DATA'][key]]).rstrip(',')
                newline = '\n'
                finalString =  valueString + newline
                transList.append(finalString)
    #If not in append mode, include all lines
    else:
        for key in dataset['DATA']:
            valueString =  " ".join([str(x) + ',' for x in dataset['DATA'][key]]).rstrip(',')
            newline = '\n'
            finalString =  valueString + newline
            transList.append(finalString)
            
    # Write transList to a file object (see xayacore writeGraph)
    fileObject = open(filepath, 'a+')
    fileObject.writelines(transList)
    fileObject.flush()
    return fileObject
        
        
        
def htmlDataset(dataset = {}, title=""):
    """ Utility function to generate HTML Table from a Dataset"""
    content = "<TABLE cellpadding=5> <caption align=top>" + title + " </caption><TR></TR><TR></TR>"
    for row in dataset['DATA']:
            content += "<TR>"
            for col in dataset['DATA'][row]:
                if row==0:
                    content += "<TH align=left bgcolor=#BBDB88>"
                else:
                    content += "<TD align=left bgcolor=#FFFAB2>"
                content += col
                if row==0:
                    content += "</TH>"
                else:
                    content += "</TD>"
            content += "</TR>"
    content += "</TABLE>"
            
        
    return content

def saveHtmlDataset(dataset = {},title="", filepath = ""):
    """ Saves a dataset in HTML format to a file,
    for easy viewing in a web browser
    """
    html = htmlDataset(dataset, title)
    fileObject = open(filepath, 'a+')
    fileObject.write(html)
    fileObject.flush()
    return fileObject
    


def viewData(dataset):

    """
    Given a dataset, print it out in reader friendly format

    """
    return pprint.pprint(dataset['DATA'])

def viewVariables(dataset):

    """

    Given a dataset, print out the heading fields in reader friendly format
    
    """
    for entry in dataset['DATA'][0]:
        pprint.pprint(str(entry) + " : " + str(dataset['VARIABLES'][str(entry)]))


def saveData(dataset={}, filepath= 'defaultFilePath'):
    """
    Saves the 'DATA' component of a dataset as an ascii file
    in XAYAcore graph format.
    """
    return xayacore.writeGraph(dataset['DATA'], filepath)

def saveVariables(dataset={}, filepath= 'defaultFilePath'):
    """
    Saves the 'VARIABLES' component of a dataset in an ascci file
    in XAYAcore graph format
    
    """
    return xayacore.writeGraph(dataset['VARIABLES'], filepath)

def readFile(filepath =""):
    """ Reads file object into a dictionary keyed to line number """
    try:
        fileobj = open(filepath, 'r')
    except IOError:
        print "File not opened, could not find", filepath
    else:
        # print "-------------------------------"
        # print
        # print "Opening file", filepath -- Disabled as adds to much "gibberish" to interpreter session when opening lost of files at once
        datatable = {}
        autonumberkey = -1
        for line in fileobj:
            autonumberkey = autonumberkey + 1
            datatable[autonumberkey] = line
        fileobj.close()
        return datatable

# def writeFile(filepath=" "):     

def getData(filepath =" "):
	""" Cleans up readFile dictionary so it can function as a relation tbl like dataset  """
	data = readFile(filepath)
	dataGraph = {}
	for key in data.keys():
		dataGraph[key] = [column.strip() for column in data[key][:-1].split(",")] # strip newline at end
	return dataGraph

        

def getVariables(filepath =""):
    """ Extracts a dictionary of VariableName: Index pairs from getData """
    data = getData(filepath)
    variables = {}
    for index in range (len(data[0])):
        variables[data[0][index]] = [index]
    return variables


# ---------- Sorting and Grouping  Functions ----------

def getSorts(dataset = {}, sortVars = [], sortOrder = 'ASC'):
    """
    Adds a SORTS component to a XAYA format dataset.
    Given a XAYA format dataset and a list of variables to sort on,
    returns the same dataset, with the addition of the SORTS component. 
    The SORTS component  is a list of keys in dataset['DATA']
    in sort order. The default sort order is ascending ('ASC').
    For descending sort order, enter 'DESC'
    Algorithm:
        # Extract the 'DATA' component of dataset to sort
        # Extract the index positions of variablse we wish to sort DATA by
        # Create a dictionary whose values include only the data we wish to sort by
        # Create a list of tuples where:
            # The first tuple element (0) is a list of the data to sort by
            # The second tuple element (1) is the dictionary key.
             #  Data headings from this list of tuples (tuple 0) have been removed
         # Sort the tuples based on the selected variables:
             # If sort order is 'ASC' -- sort ascending
             # if sort order is 'DESC' -- sort descending
        # Create a new dataset
        # Copy the original dataset to the new dataset
        # Add a new 'SORTS' component to the new dataset
        # Return the new dataset with 'SORTS' added.
        
    Note: One can later reverse the order in which data is displayed
    by reversing the 'SORTS' component. So consider using the default
    sort-order 'ASC', unless there is a compelling reason why the natural sort
    for this data would be in descending order, 'DESC'
        
    """
    sortdata =  {} # Set up a dictionary for  data that will be the basis of the sort
    newdataset = {} # set up a new dataset that will include the sort order data
    
    # Extract the 'DATA' component of dataset to sort
    data = dataset['DATA']
    variables = dataset['VARIABLES']
    
    # Extract the index positions of variables we wish to sort DATA by
    varindexlist = []
    for vars in sortVars:
        varindexlist.append(variables[vars][0])
    keylist = [] # list that will hold keys in the final sort order
    
    #Create a dictionary whose values include only the data we wish to sort by
    for row in data:
        rowlist = []
        for var in varindexlist:
            rowlist.append(data[row][var])
        sortdata[row] = rowlist
            
    # Create a list of tuples where:
        # The first tuple element (0) is a list of the data to sort by
        # The second tuple element (1) is the dictionary key.
        #  Data headings from this list of tuples (tuple 0) have been removed
    sortdatalist = [(values, row) for row, values in sortdata.items()]
    sortdatalist.pop(0)
    
    # Sort the tuples based on the selected variables:
    sortedlist = sortlist(sortdatalist)
    for tuple in sortedlist:
        keylist.append(tuple[1]) # Extract keys in ascending sort order
    if not sortOrder == 'ASC':
        keylist.reverse() # Extract keys in descending sort order

    # Create a new dataset that contains the original data and the new SORTS component.
    for key in dataset.keys():
        newdataset[key] = dataset[key]
    newdataset['SORTS'] = keylist
    return newdataset

def sortedDataset(dataset={}, sortOrder='ASC'):
    """Sorts a Dataset in Variable Order """
    # varitems = dataset['VARIABLES'].items()# Tuples with variable key, and variable index no
    varlist = [ (x, y) for y, x in dataset['VARIABLES'].items()]
    varlist.sort()
    variables = []
    for tuple in varlist:
        variables.append(tuple[1])
    sortlist = getSorts(dataset, variables,sortOrder)['SORTS']
    sorteddataset = {}
    sorteddataset['DATA'] ={}
    sorteddataset['DATA'][0] = dataset['DATA'][0]
    autonumberkey = 0
    for item in sortlist:
        autonumberkey = autonumberkey + 1
        sorteddataset['DATA'][autonumberkey] = dataset['DATA'][item]
    for key in dataset.keys():
        if key != 'DATA':
            sorteddataset[key] = dataset[key]
        
    return sorteddataset
    
    
def getGroups( dataset = {}, groupVars = []):
    """
    Adds a GROUPS component to a XAYA format dataset.
    Given a XAYA format dataset and a list of variables to group on,
    returns the same dataset, with the addition of the GROUPS component. 
    The GROUPS component contains a dictionary where keysrepresen unique groups,
    and values are the list of rows (keys) in dataset['DATA'] that are members of that group
    Algorithm:
        # Extract the 'DATA' component of dataset to group
        # Extract the index positions of variables we wish to group DATA by
        # Create a dictionary whose values include only the data we wish to group by
        # Get a list of all values to aggregate into groups
        # Create the set of unique groups
        # Assign rows of data to a particular group
    
    """
    groupdata =  {} # Set up a dictionary for  data that will be the basis of the grouping
    newdataset = {} # set up a new dataset that will include the sort order data
    
    # Extract the 'DATA' component of dataset to group
    data = dataset['DATA']
    copydata = data.copy() # Make a shallow copy  data -- so 'del' in next statement leaves original data untouched
    del copydata[0] # Get rid of the headings row in copydata -- leaves data untouched
    variables = dataset['VARIABLES']
    
    # Extract the index positions of variables we wish to group DATA by
    varindexlist = []
    for vars in groupVars:
        varindexlist.append(variables[vars][0])
        
    # Create a dictionary whose values include only the data we wish to group by
    for row in copydata:
        rowlist = []
        for var in varindexlist:
            rowlist.append(copydata[row][var])
        groupdata[row] = rowlist

    # Get a list of all values to aggregate into groups
    groupslist = groupdata.values() # Result is a list of lists -- we want a list of tuples, so can use the groups as keys in a dictionary
    
    # Convert groups from lists to tuples
    grouptuples = [tuple(group) for group in groupslist]
    
    # Create the set of unique groups
    groupset = set(grouptuples)
    
    # Initialize  a dictionary to hold the groups
    groupsdict = {}
    for group in groupset:
        groupsdict[group] = [ ]
        
    # Assign rows of data to a particular group
    for row in groupdata:
        for member in groupset:
            if tuple(groupdata[row]) == member:
                groupsdict[member].append(row)
                
    # Create a new dataset that contains the original data and the new GROUPS component.
    for key in dataset.keys():
        newdataset[key] = dataset[key]
    newdataset['GROUPS'] = groupsdict
    return newdataset
    

def getTypes(dataset = {}, typesGraph = {}):
    """
    Adds a TYPES component to a dataset, and casts the data based
    on the typesGraph (a XAYA format graph) whose nodes are the variable names
    and whose edges are the data type for that variable.
    Default data type is string.
    Data of types 'CATEGORICAL' and 'TEXT', remains as string. Data of
    type 'INTEGER' is cast to via the python fn int(). Data of type 'NUMERICAL' is
    cast via the python fn float()
    Algorithm:
        # Check that variables in dataset match variables in typesGraph
        # Check that there are no unknown types in typesGraph
        # Extract a sorted list  of the index positions and names of each variable
        # Create a dictionary with data values cast to appropriate types
            # 'TEXT' and 'CATEGORICAL' are left as is
            # 'INTEGER' is cast via int() fn
            # 'NUMERICAL' is cast via float() fn
        # Create a new dataset that contains the original data and the new TYPES component.
    """

    # Set up of variables needed later in function
    data = dataset['DATA']
    copydata = data.copy() # Make a shallow copy  data -- so 'del' in next statement leaves original data untouched
    del copydata[0] # Get rid of the headings row in copydata -- leaves data untouched
    variables = dataset['VARIABLES']
    vars = variables.keys()
    typevars = typesGraph.keys()
    typedata =  {} # Set up a dictionary for  data that is cast to type
    newdataset = {}# set up a new dataset that will include the Types component
    tocast = ['INTEGER', 'NUMERICAL']
    tonotcast = ['TEXT', 'CATEGORICAL']
    alltypes = ['INTEGER', 'NUMERICAL','TEXT', 'CATEGORICAL']
    
    
    # Check that variables in dataset match variables in typesGraph
    for variable in vars:
        if variable not in typevars:
            print 'There is a mismatch between Dataset Variables and the typesGraph'
            return newdataset
        
    # Check thatthere are no unknown types in the typesGraph
    typevalues = [value[0] for value in typesGraph.values()]
    for type in typevalues:
        if type not in alltypes:
            print 'There is an unknown data type in typesGraph'
            return newdataset
    # Extract a sorted list  of the index positions and names of each variable 
    varitemslist = [(value[0], key) for key, value in  variables.items()]
    varitemslist.sort()
        
    # Create a dictionary with data values cast to appropriate types
    typedata[0] = data[0]
    for row in copydata:
        rowlist = []
        for varitem in varitemslist:
            castitem = data[row][varitem[0]]
            typeitem = typesGraph[varitem[1]][0]
            if typeitem  in tonotcast: # Leave 'TEXT' and 'CATEGORICAL' as is
                rowlist.append(castitem)
            elif  typeitem == 'INTEGER':
                rowlist.append(int(float(castitem))) # Need to cast to float first for things like '1839.00'
            else:
                rowlist.append(float(castitem))
        typedata[row] = rowlist
        
    # Create a new dataset that contains the original data and the new TYPES component.
    for key in dataset.keys():
        if key != 'DATA':
            newdataset[key] = dataset[key]
    newdataset['TYPES'] = typesGraph
    newdataset['DATA'] = typedata
    return newdataset
 
def filterDataset(dataset = {}, filterVar = '', filterValues = []):
    """
    Filters a XAYA format dataset on a single variable for a list of filter values.
    
    Given a XAYA format dataset, a filterVar and a list of filterValues,
    this function returns a dataset containing only those rows that contain the filter values.
    If you wish to filter on multiple variables -- you can run this function several times.
    
    Examples:
    >>> filteredbooks1 = xayastats.filterDataset(books, 'PositiveReviews', [250])
    # returns only those rows from books dataset which have 250 positive reviews
    >>> filteredbooks2 = xayastats.filterDataset(books, 'Author', ['Mishtu', 'Ian'])
    # returns only those rows from books dataset whose authors are either Ian or Mishtu
    # Note -- be if the dataset is cast to datatypes, you must have the correct datatype in your list.
            For example, 250 is not the same as '250' -- one is an integer and the other is a string
    
    
    
    
    Algorithm:
        # Extract the 'DATA' component of dataset to filter
        # Extract the index positions of variable we wish to filter by
        # Build a filtered dataset"
            By looping through data rows and checking the variable (at index position)
            And adding only those rows whose value is in the filterValues list
        
    """
     # Set up of variables needed later in function
    data = dataset['DATA']
    datarows = data.keys()[1:]
    variables = dataset['VARIABLES']
    varIndex = variables[filterVar][0]
    vars = variables.keys()
    filterdataset = {}# set up a filter dataset
    filterdataset['DATA'] = {}
    filterdataset['DATA'][0] = data[0]
    for row in datarows:
        
        if data[row][varIndex] in filterValues:
            filterdataset['DATA'][row] = data[row]
    # Create a new dataset that contains the original data and the new TYPES component.
    for key in dataset.keys():
        if key != 'DATA':
            filterdataset[key] = dataset[key]
    return filterdataset
            

def joinDatasets(parentDataset={}, childDataset={}, joinKeys=[]):
    """
    This function approximates a relational join on two datasets with a common key.
    It assumes the common keys have identical names. A one-to-many relationship is
    assumed between the parentDataset and childDataset. A special case being a one-to-one
    relationship between the two datasets.
    Algorithm:
        For each dataset
            Create a Graph with joinKeys as nodes, and rows for a joinKey as arcs
        For each JoinKey in Parent Dataset (should be a single row)
            For each JoinKey in Child Dataset matching parent Joinkey
        
    """

# ---------- Data Extraction and Type-Casting  Functions ----------

def getDatalist (dataGraph = {}, varGraph = {}, variable = "" ):
    """ Produces a data list for the via dataset and variables dictionary for a named variable"""
    # List needs to be converted if data is to be treated as Integer or Numerical (floats)
    # Default is to treat data as Categorical
    data = dataGraph
    vars = varGraph
    var = variable
    datalist = []
    """ Extracts a Variable Column as a datalist, using dataset and column dictionaries"""
    keys = data.keys()
    keys.remove(0)
    for key in keys:
        datalist.append(data[key][varGraph[var][0]])
    return datalist

def castDatalistToNumerical(list = []):
    """ Converts a list to float number values """
    datalist = list
    numberlist = []
    for item in datalist:
        numberlist.append(float(item))
    return numberlist

def getNumberslist(dataGraph = {}, varGraph = {}, variable = ""):
	return castDatalistToNumerical(getDatalist(dataGraph, varGraph, variable))


def castDatalistToInteger(list = []):
    """ Converts a list to float number values """
    datalist = list
    numberlist = []
    for item in datalist:
        numberlist.append(int(item))
    return numberlist

def getIntegerslist(dataGraph = {}, varGraph = {}, variable = ""):
	return castDatalistToInteger(getDatalist(dataGraph, varGraph, variable))


def testTypes(item = None):
    """
    A set of tests to distinguish between the various XAYAstats data types:
    TEXT, CATEGORICAL, INTEGER, NUMERICAL
    Definition:
        Item is None or empty string, there is no data
        Items must be either strings or numbers according to Python
        letters are not numbers
        text has white space
        integers do not straggle over the decimal line
    
    """
    # Default case -- item is None, or empty string returns no data
    if item == None or item == "":
        return 'NODATA'
    else:
        # Items must be either strings or numbers according to Python
        try:
            float(item)
        except TypeError:
            print "Item is not one of the following: TEXT, CATEGORICAL, INTEGER, NUMERICAL"
            return 'UNDEFINED'
        # Letters are not numbers
        except ValueError:
                # text has white space
                if list(item).count(' ') == 0:
                    return 'CATEGORICAL'
                else:
                    return 'TEXT'
    # integers do not straggle over the decimal line
    if int(float(item)) == float(item): # int(float(item) prevents ValueError for items like '24.0'
        return 'INTEGER'
    else:
        return 'NUMERICAL'

# ---------- genStats Functions ----------

def getSummarystats(dataset = {}, variable = ""):
    """
    Calculates a set of basic statistics on variable in a dataset
    and returns results as a dictionary of summary statistics.
    Note results are for viewing ease, but are not in XAYAstats
    dataset format.
    
    """
    data = getNumberslist(dataGraph = dataset['DATA'], varGraph = dataset['VARIABLES'], variable = variable)
    return summarystat(data)

def summarizedDataset(dataset={}):
    """Summarizes a dataset.
    Stage 1: Summarizes numerical variables
    Stage 2: Summarizes numerical variables, grouped by categorical variables. 
    """
    # Get Variables into a list, sorted by variable position
    varlist = [ (x, y) for y, x in dataset['VARIABLES'].items()]
    varlist.sort()
    variables = []
    for tuple in varlist:
        variables.append(tuple[1])
    # Loop through variables
    summarydata = {}
    summarydata['DATA'] = {}
    summarydata['DATA'][0] = ["Variable", "Min", "Max", "Mean", "Median", "Range", "SD", "CV"]
    summarydata['VARIABLES'] = {"Variable" : [0],
        "Min": [1],
        "Max": [2],
        "Mean": [3],
        "Median": [4],
        "Range": [5],
        "SD": [6],
        "CV": [7]}
    autonumberkey = 0
    for var in variables:
        # Test that variables are numerical
        datalist = getDatalist(dataset['DATA'],dataset['VARIABLES'], var)
        datalist.sort()
        try: float(datalist[0])
        except ValueError: continue
        try: float(datalist[-1])
        except ValueError: continue
        # If numerical, calculate summary stats
        autonumberkey = autonumberkey + 1
        summarygraph = getSummarystats(dataset,var)
        # Move data from individual graphs to dataset format
        summarydatalist = []
        summarydatalist.append(var)
        summarydatalist.append(summarygraph['min'][0])
        summarydatalist.append(summarygraph['max'][0])
        summarydatalist.append(summarygraph['mean'][0])
        summarydatalist.append(summarygraph['median'][0])
        summarydatalist.append(summarygraph['range'][0])
        summarydatalist.append(summarygraph['sd'][0])
        summarydatalist.append(summarygraph['cv'][0])
        summarydata['DATA'][autonumberkey] = summarydatalist
     
    return summarydata
    
def getHistograph(dataset = {}, variable = ""):
     """
     Calculates a histogram-like summary on a variable in a dataset
     and returns a dictionary. The keys in the dictionary are unique items
     for the selected variable. The values of each dictionary key, is the number
     of times the unique item occured in the data set
     """
     data = getDatalist(dataGraph = dataset['DATA'], varGraph = dataset['VARIABLES'], variable = variable)
     return histograph(data)

def sortHistograph(histograph = {}, sortOrder = 'DESC'):
    """
    Sorts an histograph to make it easier to view. The default is
    descending (DESC) order (most to least frequent). Enter 'ASC' to produce
    an histogram in ascending order (least to most frequent).
    """
    sortedHist = []
    sortedHist = sortlist([(value,key)for key,value in histograph.items()])
    if not sortedHist == 'ASC':
        sortedHist.reverse()
    return sortedHist

def minstat(list = [ ]):
    """ Returns minimum value in a list or tuple"""
    return min(list)

def maxstat(list = [ ]):
    """ Returns minimum value in a list or tuple"""
    return max(list)

def rangestat(list = [ ]):
    """ Returns the absolute range of values in a list or tuple""" 
    return abs(maxstat(list) - minstat(list))


def sumstat(*L):
    """
    Sums a list or a tuple L
    Modified from pg 80 of Web Programming in Python
    
    """
    if len(L) == 1 and \
       ( isinstance(L[0],types.ListType) or \
         isinstance (L[0], types.TupleType) ) :
        L = L[0]
    s = 0.0
    for k in L:
        s = s + k
    return s
# Consider changing so uses the much simpler built-in sum() fn. 

def sumsqstat(*L):
    """ Sum of squares for a list or a tuple L"""
    if len(L) == 1 and \
       ( isinstance(L[0],types.ListType) or \
         isinstance (L[0], types.TupleType) ) :
        L = L[0]
    s = 0.0
    for k in L:
        sq = k * k # Calculates the Square
        s = s + sq # Sums the Square
    return s
# Consider changing so uses the much simpler built-in sum() fn

def meanstat(n):
    """ Calculates mean for a list or tuple """
    mean = sumstat(n)/float(len(n))
    return mean

def medianstat(n):
    """
    Calculates median for a list or tuple
    Modified from pg 347 Zelle's CS intro book,
    Python Programming, an Introduction to Computer Science
    """
    s = n[:]
    s.sort()
    size = len (n)
    midPos = size/2
    if size % 2 == 0:
        median = (s[midPos] + s[midPos - 1]) /2.0
    else:
        median = s[midPos]
    return median

def dlist(list = [ ]):
    """ Calculates a list of Deviations from Mean"""
    diffs = [ ]
    mean = meanstat(list)
    for k in list:
        diff = k - mean
        diffs.append(diff)
    return diffs

def varstat(list = [ ]):
    """ Calculates the Variance for a list or tuple L"""
    devs = dlist(list)
    sumdevs = sumsqstat(devs)
    var = sumdevs/(len(list)-1.0)
    return var

def sdstat(list = [ ]):
    """ Calculates the Variance for a list or tuple """
    sd = sqrt(varstat(list))
    return sd


def cvstat(list = [ ]):
    """ Calculates the Coefficient of Variation"""
    cv = sdstat(list)/meanstat(list) * 100
    return cv 

def summarystat(list = [ ]):
    """Summary Statistics for a List or Tuple"""
    statsGraph = {}
    min = minstat(list)
    max = maxstat(list)
    range = rangestat(list)
    mean = meanstat(list)
    median = medianstat(list)
    sd = sdstat(list)
    cv = cvstat(list)
    statsGraph['min'] = [min]
    statsGraph['max'] = [max]
    statsGraph['range'] = [range]
    statsGraph['mean'] = [mean]
    statsGraph['median'] = [median]
    statsGraph['sd'] = [sd]
    statsGraph['cv'] = [cv]
    return statsGraph

    #Alternate summarystat implementation (as Xaya format graph)
   # valuelist = [min,max,mean,median,sd,cv]
   # keytuple = ('min','max','mean','median','sd','cv')
   # for key in range(len(keytuple)):
   #     statsGraph[key] = valuelist[key]
   # return statsGraph
   # screwing up on indices and tuple list dict diffs



def zlist(list = [ ]):
    """Calculates z scores for a list or tuple"""
    zeds = []
    mean = meanstat(list)
    sd = sdstat(list)
    for k in list:
        zed = (k - mean)/sd
        zeds.append(zed)
    return zeds

def rlist( list = [ ]):
    """Calculates Range scores with values between 0 and 1"""
    rrs = []
    min = minstat(list)
    range = rangestat(list)
    for k in list:
        r = (k - min)/float(range)
        rrs.append(r)
    return rrs

def histograph(list = [ ]):
	"""
	A histograph is a histogram where the unique items
	in a list are keys, and the counts of each item is the value
	for that key. The format is in XAYA graph format (values are lists)
	Definition:
		Get the set of distinct items in a list
		Count the number of times each item appears
		
	
	"""
	histoGraph = {}
	# Get the set of distinct items in a list
	distinctItems = set(list)
	# Count the number of times each item appears
	for item in distinctItems:
		histoGraph[item] = [list.count(item)]
	return histoGraph

# Add assertions
# assert meanstat(zscores) == 0
# assert sdstat(zscores) == 1.0
# assert minstat(rscores) == 0.0
# assert maxstat(rscores) == 1.0



