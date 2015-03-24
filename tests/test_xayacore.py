#!/usr/bin/env python
"""
BeginDate: 20040907
CurrentRevisionDate:20040921
Development Version : core 001
Release Version: pre-release

Author(s): Mishtu Banerjee, Tyler Mitchell
Contact: mishtu@harmeny.com

Copyright: The Authors
License: Distributed under MIT License
    [http://opensource.org/licenses/mit-license.html]
    
Environment: Programmed and tested under Python 2.3.3 on Windows 2000.
    Database Access: Psycopg and Postgres 7.4
    
Dependencies:
    Python Interpreter and base libraries.
    unittest
    xayacore

# test_xayacore.py  renamed from test_xayacore August 18, 2005    
    


"""

import unittest
import xayacore
import os

class xayacore_readGraphTest(unittest.TestCase):

#Current List of TestCases for readGraph
    #Test Normal Case -- DONE
    #Test Case -- No File at Path Location -- DONE
    #Test Case -- File has missing final newline -- LATER -- CURRENTLY HANDLED
    #Test Case -- Key without values -- DONE -- "empty dictionary"
    #Test Case -- values without Key -- DONE -- "empty dictionary"
    #Test Case(s) List Parentheses used -- LATER -- functionality has not been added yet
    # Test Case??? -- File is not ascii. -- LATER
#PreConditions:
    # Assume Ascii, or Unitext file
    # Assume each line a Key:ValueList pairing
    # Assume XAYA or YAML format

#PostCondtions:
    #Outputs a Dictionary
    #Dictionary has Key, Value-list pairs.

    def test_001_NormalCase(self):
        """ readGraphTest_001_NormalCase: Tests the Normal Case with a XAYA format ascii file"""
        self.assertEqual(xayacore.readGraph("/XAYA/devcore/test/test_DataDictionary_X001.txt"),
                         {'StandStructureID': ['1', ''], 'PolygonID': ['1', ''], 'StandStructureDescription': ['']})

    def test_002_NoFile(self):
          """ readGraphTest_002_NoFile: Test the case NoFile  where the file doesn't exist at the location"""
          self.assertEqual(xayacore.readGraph("/bad/path/to/no/file"),'File not opened, could not find/bad/path/to/no/file')

    def test_003_EmptyFile(self):
        """ readGraphTest_003_EmptyFile: Test  the case EmpytFile to see if the input file was empty, i.e. returns an empty dict"""
        self.assertEqual(xayacore.readGraph("/XAYA/devcore/test/test_emptyfile.txt"),{})

    def test_004_EmptyDictionary(self):
        """ readGraphTest_004_EmptyDictionary: Test the case EmptyDictionary where file contains only the ":" delimiter. Should return an empty dictionary """
        # Single ":" delimiter on a line
        self.assertEqual(xayacore.readGraph('/XAYA/devcore/test/test_emptydictionary.txt'),{'': ['']})
        # Multiple "." delimiters on a line
        self.assertEqual(xayacore.readGraph('/XAYA/devcore/test/test_emptydictionary2.txt'),{'': ['']})
        # Multiple ":" delimiters on several lines
        self.assertEqual(xayacore.readGraph('/XAYA/devcore/test/test_emptydictionary3.txt'),{'': ['']})


    def test_005_NoDelimiter(self):
        """ readGraphTest_005_NoDelimiter: Tests case NoDelimiter --  if readGraph bails on lines with various bad formats that have no delimiter of ":" """
        #Case 1 -- 2 empty lines -- Interface Changed December 19, 2005 so empty lines silently pass
        # self.assertRaises(IndexError, xayacore.readGraph, '/Xaya/devcore/test/test_badformat.txt')
        #Case 2 -- single line with "{'-------'  '----'}"
        # Interface Changed February 21, 2006 so non-delimiter lines silently pass -- deal w invisible chars
        #self.assertRaises(IndexError, xayacore.readGraph, '/Xaya/devcore/test/test_badformat2.txt')
        #Case 3 -- Empty Dictionary case, followed by a single line of text
        # Interface Changed February 21, 2006 so non graph format lines pass
        # self.assertRaises(IndexError, xayacore.readGraph, '/Xaya/devcore/test/test_badformat3.txt')
        #Case 4 -- Data from Normal Case -- now with two blank lines added in midst of correctly formated dictionary
        # -- Interface Changed December 19, 2005 so empty blanks silently pass
        # self.assertRaises(IndexError, xayacore.readGraph, '/Xaya/devcore/test/test_badformat4.txt')

  
class xayacore_shelveGraphTest(unittest.TestCase):
    def setUp(self):
        """ Sets up a graph for the tests on shelveGraph"""
        self.graph_shelveGraph = {'BillInventory': ['Objects_X001.txt'],
                 'StoredInventory': ['Objects_X001.txt', 'datMeasurements_X001.txt','datNewData20040917added.txt'],
                 'MiniForestInventory': ['Objects_X001.txt', 'Schema_X001.txt', 'Measures_X001.txt', 'MeasureTypes_X001.txt', 'DataDictionary_X001.txt', 'datStandStructures_X001.txt', 'datPolygons_X001.txt', 'datPlots_X001.txt', 'datTrees_X001.txt', 'datMeasurements_X001.txt'],
                 'TylerInventory': ['Schema_X001.txt', 'Measures_X001.txt', 'MeasureTypes_X001.txt', 'DataDictionary_X001.txt', 'datStandStructures_X001.txt', 'datPolygons_X001.txt', 'datPlots_X001.txt', 'datTrees_X001.txt', 'datMeasurements_X001.txt'],
                 'ShawnInventory': ['Objects_X001.txt', 'Schema_X001.txt', 'datStandStructures_X001.txt', 'datPolygons_X001.txt'],
                 'IanInventory': ['Objects_X001.txt', 'datMeasurements_X001.txt']
                 }
        
    def test_001_NormalCase(self):
        """ shelveGraphTest_001_NormalCase: Tests the NormalCase of the graph read into shelf being returned by shelf"""
        self.assertEqual(xayacore.shelveGraph(self.graph_shelveGraph, 'shelvegraphtestfile'),self.graph_shelveGraph)
        os.remove('shelvegraphtestfile') # tears down shelf file created in this test

    def test_002_EmptyGraph(self):
        """ shelveGraphTest_002_EmptyGraph: Tests the case  EmptyGraph of an emptygraph being shelved to a default location"""
        self.assertEqual(xayacore.shelveGraph(),{})
        os.remove('defaultFilePath') # tears down shelf file created in this test
        #Note 20040921 -- This test will fail if default locn already has some data. Refactor test. has to check than wipe any prev data

    def test_003_NotAGraph(self):
        """ shelveGraphTest_003_NotAGraph: Tests the case NotAGraph of trying to use a non-dictionary  data structure as input """
        self.assertRaises(AttributeError,xayacore.shelveGraph,[1,2,3,4,5,6])
        os.remove('defaultFilePath')

    def test_004_StringVsInteger(self):
        """ shelveGraphTest_004_StringVsInteger: Tests case StringVsInteger -- that strings as keys work, integers as keys fail """
        self.assertEqual(xayacore.shelveGraph({'1':'one', '2': 'two'}),{'1':'one', '2': 'two'})
        os.remove('defaultFilePath') # tears down shelf file created in this test
        self.assertRaises(TypeError, xayacore.shelveGraph,{1:'one', 2: 'two'})
        os.remove('defaultFilePath')

   # def tearDown(self): # tear downs done at fn level instead -- otherwise runs after each method in subclass
    #    """ Tears down the shelf files created during testing"""
    #   os.remove('defaultFilePath')
    #   os.remove('shelvegraphtestfile')
    # REFACTOR SO THAT tearDown TESTS FOR FILE BEFOR ATTEMPTING TO DELETE. WILL WORK THEN.
        
    

class xayacore_transValueToKey(unittest.TestCase):

# Tests for transValueToKey:
    # testNormalCase_transValueToKey -- Read in a Keylist, generate a graph per keylist
    # testEmptyKeyList_transValueToKey -- Read in an emplty keylist, generate all graphs
    # testNoSuchGraph_transValueToKey -- Read in a Graph that does not exits -- generates a NameError -- what kind??
    #testNoSuchKey_transValueToKey -- Read in a Key, that is not in the Graph
    
    def setUp(self):
       self.graph_transValueToKey = {
           'Key1' : ['Key1V1', 'Key1V2', 'Key1V3', 'Key1V4','Key1V5'],
           'Key2' : ['Key2V1', 'Key2V2', 'Key2V3', 'Key2V4'],
           'Key3' : ['Key3V1', 'Key3V2', 'Key3V3'],
           'Key4' : ['Key4V1', 'Key4V2'],
           'Key5' : ['Key5V1'],
           'Key6' : [],
           'Key7' : None
           }

    def test_001_NormalCase(self):
        """ transValueToKeyTest_001_NormalCase: Tests NormalCase where Graph and Key input leads to output of Indexed Graph of  values for that Key"""
        normaldata = xayacore.transValueToKey(self.graph_transValueToKey,'Key4').keys()
        normaldata.sort()
        self.assertEqual(normaldata,['Key4V1','Key4V2'])

    #def test_002_NoSuchGraph(self):
    #    """ transValueToKeyTest_002_NoSuchGraph:Tests the case where the named input graph is missing"""
    #    self.assertRaises(NameError,xayacore.transValueToKey,nosuchgraph)
    #NameError seems to screw up unittest -- since nosuchgraph is undefined .....

    def test_003_NoSuchKey(self):
        """ transValueToKeyTest_003_NoSuchKey: Tests the case NoSuchKey where the Key input does not exist in the graph"""
        self.assertEqual(xayacore.transValueToKey(self.graph_transValueToKey,'NoKey4'),{})

    def test_004_NoInputParams(self):
        """ transValueToKeyTest_004_NoInputParams: Tests the case NoInputParams where No Input Parameters given"""
        self.assertEqual(xayacore.transValueToKey(),{})

    def test_005_NotAGraph(self):
        """ transValueToKeyTest_005_NotAGraph: Tests the case  NotAGraph where a non-graph data type input"""
        self.assertRaises(AttributeError,xayacore.transValueToKey,[1,2,3,4])

    
class xayacore_bindGraphsByValues(unittest.TestCase):

    def setUp(self):
        # Set Up a ParentGraph as a Measures Table
        self.graphMeasures = {
            'datPlotStructures_X001.txt': ['PlotStructureID', 'PlotStructureDescription'],
            'datTrees_X001.txt': ['TreeID', 'TreeNo', 'PlotID', 'TreeSpp'],
            'datStandStructures_X001.txt': ['StandStructureID', 'StandStructureDescription'],
            'datPlots_X001.txt': ['PlotID', 'PolygonID', 'PlotArea', 'PlotProtocol', 'PlotStructureID'],
            'datMeasurements_X001.txt': ['MeasurementID', 'TreeID', 'MeasureDate', 'Height', 'Diameter', 'Age', 'Damaged'],
            'datPolygons_X001.txt': ['PolygonID', 'StandStructureID', 'PolyArea', 'PolyLeadSpp'],
            'datProtocols_X001.txt': ['ProtocolID', 'ProtocolName', 'ProtocolDescription']
            }
        #Set Up a ChildGraph as a Data Table (for tree data in this example)
        self.graphTreeData =  {'1': ['1', '1', '1', 'Fd'],
                               '3': ['3', '1', '2', 'At'],
                               '2': ['2', '2', '1', 'Pl'],
                               '5': ['5', '3', '2', 'Fd'],
                               '4': ['4', '2', '2', 'At']
                               }
        
        self.alist = [1,2,3,4]
        
        
    def test_001_NormalCase(self):
            """ bindGraphsByValuesTest_001_NormalCase: Tests NormalCase where a filtered version of childgraph is returned based on key:value parent criteria"""
            self.assertEqual(xayacore.bindGraphsByValues(self.graphMeasures,'datTrees_X001.txt','TreeSpp',self.graphTreeData), {'1': 'Fd', '3': 'At', '2': 'Pl', '5': 'Fd', '4': 'At'})

    def test_002_NoSuchGraph(self): pass
    """ bindGraphByValuesTest_002_NoSuchGraph: Tests case where named graph does not exist """
    # Refactor test to work. Problems similar to those for test 2 in transValueToKey
    
    def test_003_NoSuchKey(self):
        """ bindGraphsByValuesTest_003_NoSuchKey: Tests case where keys missing in either ParentGraph or ChildGraph """
        # Key missing in ParentGraph 'graphMeasures'
        self.assertRaises(KeyError,xayacore.bindGraphsByValues, self.graphMeasures,'NoKeydatTrees_X001.txt','TreeSpp',self.graphTreeData)
        # Key missing in ChildGraph 'graphTreeData' (Key in ChildGraph is a Value for the selected key in ParentGraph)
        self.assertRaises(KeyError,xayacore.bindGraphsByValues,self.graphMeasures,'datTrees_X001.txt','NoKeyTreeSpp',self.graphTreeData)

    def test_004_NoInputParams(self):
        """ bindGraphsByValuesTest_004_NoInputParams: Tests case where input defaults are taken """
        self.assertEqual(xayacore.bindGraphsByValues(), {})

    def test_005_NotAGraph(self):
        """ bindGraphsByValuesTest_005_NotAGraph: Tests case where either ParentGraph or ChildGraph not Dictionaries(Graphs) """
        # NotAGraph for expected ParentGraph
        self.assertRaises(AttributeError, xayacore.bindGraphsByValues,self.alist,'datTrees_X001.txt','TreeSpp',self.graphTreeData)
        # NotAGraph for expected ChildGraph
        self.assertRaises(TypeError, xayacore.bindGraphsByValues,self.graphMeasures,'datTrees_X001.txt','TreeSpp',self.alist)

    def test_006_MutableKey(self):
        """ bindGraphsByValuesTest_006_MutableKey: Tests case where attempt to use a non-hashable value as a key """
        self.assertRaises(TypeError, xayacore.bindGraphsByValues,self.graphMeasures,self.alist,'TreeSpp',self.graphTreeData)
        self.assertRaises(TypeError, xayacore.bindGraphsByValues,self.graphMeasures,'datTrees_X001.txt',self.alist, self.graphTreeData)
    
class xayacore_transListToGraph(unittest.TestCase):
    def setUp(self):
        self.alist = [1, 2, 3, 4]
        self.morecomplexlist = [1,'two', [1,2,3], ('a','b','c'),{'akey' : 'avalue', 1: 'one'}]
        self.agraph = {'one' : 1, 'two': 2}
        self.astring = 'this is a string'

    def test_001_NormalCase(self):
        """ transListToGraphTest_001_NormalCase: Tests examples of normal list input """
        self.assertEqual(xayacore.transListToGraph(self.alist), {'1': [1], '3': [3], '2': [2], '4': [4]})
        self.assertEqual(xayacore.transListToGraph(self.morecomplexlist), {'1': [1], '[1, 2, 3]': [[1, 2, 3]],
                                                                          'two': ['two'], "('a', 'b', 'c')": [('a', 'b', 'c')],
                                                                          "{1: 'one', 'akey': 'avalue'}": [{1: 'one', 'akey': 'avalue'}]})

    def test_002_EmptyList(self):
        """ transListToGraphTest_002_EmptyList: Tests case where input is an empty list == NoInputParams """
        self.assertEqual(xayacore.transListToGraph(), {})

    def test_003_NotAList(self):
        """ transListToGraphTest_003: Tests cases where input is a Graph or a String  """
        # Result Graph has keys == values
        self.assertEqual(xayacore.transListToGraph(self.agraph), {'two': ['two'], 'one': ['one']})
        # Result Graph has keys == unique charachters in string
        self.assertEqual(xayacore.transListToGraph(self.astring), {'a': ['a'], ' ': [' '], 'g': ['g'], 'i': ['i'],
                                                                       'h': ['h'], 'n': ['n'], 's': ['s'], 'r': ['r'], 't': ['t']})
        

class xayacore_findAllPaths(unittest.TestCase):

    def setUp(self):
        # Graph from 'Python Patterns -- Implementing Graphs' by GvR. At http://www.python.org/doc/essays/graphs.html
        self.guidoGraph = {'A': ['B', 'C'], 'C': ['D'], 'B': ['C', 'D'], 'E': ['F'], 'D': ['C'], 'F': ['C']}
        # A reasonably complex model of one-to-many (parent-child) relationships in a relational db model of Forest Inventory
        self.forestryDBSchema = {'StandStructure': ['Polygon', 'Plot', 'RolledUpStandTable', 'RolledUpGMStandTable'],
                                 'Tree': ['TreeMeasurements', 'GrowthModelData'],
                                 'Polygon': ['Plot'], 'PlotMeasurements': ['StandTable', 'GrowthModelStandTable'],
                                 'Plot': ['Tree', 'CurrentStandTable', 'PlotSummary', 'PlotMeasurements']}
        # A graph with cycles
        self.cycleGraph = {'a' : ['b', 'e'], 'b' : ['c'], 'c' : ['d'], 'd' : ['a'], 'e' : ['f'], 'f' : ['a'], 'g' : ['h', 'd'], 'h' : ['c'] }
        # A graph based on the Safe Attack Tree on pg 321 (fig 21.2) of Bruce Schneier’s “Secrets and Lies"     
        self.safeattackTree = {'Threaten' : ['Get Combo from Target'],
                               'Blackmail' : ['Get Combo from Target'],
                               'Evesdrop' : ['Get Combo from Target'],
                               'Bribe' : ['Get Combo from Target'],
                               'Get Combo from Target' : ['Learn Combo'],
                               'Find Written Combo' : ['Learn Combo'],
                               'Learn Combo' : ['Open Safe'],
                                'Pick Lock' : ['Open Safe'],
                               'Cut Open Safe' : ['Open Safe'],
                                'Install Improperly' : ['Open Safe']}
  
    def test_001_NormalCase(self):
        """ findAllPathsTest_001_Normal Case:  Tests cases where non-cyclic paths found """
        # Correctly finds all paths for the graph structure used in GvR's "Python Patterns -- Implementing Graphs"
        self.assertEqual(xayacore.findAllPaths(self.guidoGraph,'A','C'), {"['A', 'C']": ['A', 'C'],
                         "['A', 'B', 'C']": ['A', 'B', 'C'],
                         "['A', 'B', 'D', 'C']": ['A', 'B', 'D', 'C']})
        # Misses "corner case" where there is a second path right through the finish node C (a cycle):
            # E-->F-->C-->D-->C
        self.assertEqual(xayacore.findAllPaths(self.guidoGraph,'E','C'), {"['E', 'F', 'C']": ['E', 'F', 'C']})
        # Correctly finds acyclic paths on two branches from start node G in a graph with cycles
        self.assertEqual(xayacore.findAllPaths(self.cycleGraph,'g','a'), {"['g', 'h', 'c', 'd', 'a']": ['g', 'h', 'c', 'd', 'a'],
                                                                               "['g', 'd', 'a']": ['g', 'd', 'a']})
        #Misses "corner case" where there is a second path through the start node a (another cycle):
            # a-->b-->c-->d-->a-->e--f 
        self.assertEqual(xayacore.findAllPaths(self.cycleGraph, 'a', 'f'), {"['a', 'e', 'f']": ['a', 'e', 'f']})
        # Two examples of paths through a database schema modelling forest inventory data relationships
        self.assertEqual(xayacore.findAllPaths(self.forestryDBSchema, 'StandStructure', 'GrowthModelData'), {"['StandStructure', 'Plot', 'Tree', 'GrowthModelData']": ['StandStructure', 'Plot', 'Tree', 'GrowthModelData'],
                                                                                                        "['StandStructure', 'Polygon', 'Plot', 'Tree', 'GrowthModelData']": ['StandStructure', 'Polygon', 'Plot', 'Tree', 'GrowthModelData']})
        self.assertEqual( xayacore.findAllPaths(self.forestryDBSchema, 'Plot', 'StandTable'), {"['Plot', 'PlotMeasurements', 'StandTable']": ['Plot', 'PlotMeasurements', 'StandTable']})
        # Two examples of opening a safe. The costly way and the lucky way.
        self.assertEqual(xayacore.findAllPaths(self.safeattackTree, 'Bribe', 'Open Safe'), {"['Bribe', 'Get Combo from Target', 'Learn Combo', 'Open Safe']": ['Bribe', 'Get Combo from Target', 'Learn Combo', 'Open Safe']})
        self.assertEqual(xayacore.findAllPaths(self.safeattackTree, 'Find Written Combo', 'Open Safe'), {"['Find Written Combo', 'Learn Combo', 'Open Safe']": ['Find Written Combo', 'Learn Combo', 'Open Safe']})

    def test_002_NoSuchPath(self):
        """ findAllPathsTest_002_NoSuchPath: Tests cases where the path does not exist   """
        # No Path, only one root node
        self.assertEqual(xayacore.findAllPaths(self.guidoGraph, 'E', 'B'), {})
        # No path, as both nodes are roots
        self.assertEqual(xayacore.findAllPaths(self.guidoGraph, 'E', 'A'), {})

    def test_003_NoSuchNode(self):
        """ findAllPathsTest_003_NoSuchNode: Tests cases where start or end node or both do not exist """
        self.assertEqual(xayacore.findAllPaths(self.guidoGraph, 'X', 'A'), {})
        self.assertEqual(xayacore.findAllPaths(self.guidoGraph, 'E', 'X'), {})
        self.assertEqual(xayacore.findAllPaths(self.guidoGraph, 'X', 'Y'), {})

    def test_004_StartIsEnd(self):
        """  findAllPathsTest_004_StartIsEnd: Tests case of a single node path """
        self.assertEqual(xayacore.findAllPaths(self.guidoGraph, 'C', 'C'), {"['C']": ['C']})

    def test_005_NoInputParams(self):
        """  findAllPathsTest_005_NoInputParams: Tests case where defaults inputs are taken """
        self.assertEqual(xayacore.findAllPaths(), {})

    def test_006_NotAGraph(self):
        """ findAllPathsTest_006_NotAGraph: Tests cases where inputs are not graphs """
        # Objects lacking 'has_key' attribute, raise error when try and use nodes as keys
        self.assertRaises(AttributeError, xayacore.findAllPaths,['This', 'Is', 'A', 'List'], 'This', 'List')
        self.assertRaises(AttributeError, xayacore.findAllPaths, 'This is a String', 'This', 'String')
        # Wrong Object, No Nodes, give an Empty Graph.
        #NOTE: CONSIDER EXPLICITLY RAISING AN ERROR HERE
        self.assertEqual(xayacore.findAllPaths(['This', 'Is', 'A', 'List']), {})
        self.assertEqual(xayacore.findAllPaths('This is a String'), {})

class xayacore_findRootsLeaves(unittest.TestCase):
    def setUp(self):
        """Test cases from various Neural Network Models in "Blondie24" by David B Fogel."""
        # Adapted  from Blondie 24 figure 6, pg 41 -- perceptron model with hidden lares
        self.perceptron = {'InputNeuron1' : ['HiddenNeuron1', 'HiddenNeuron2'],
                           'InputNeuron2' : ['HiddenNeuron1', 'HiddenNeuron2'],
                           'InputNeuron3' : ['HiddenNeuron1', 'HiddenNeuron2'],
                           'HiddenNeuron1' : ['OutputNeuron1', 'OutputNeuron2'],
                           'HiddenNeuron2' : ['OutputNeuron1', 'OutputNeuron2']}
        # Adapted from Blondie 24 figure 7, pg 43 -- structure of network to calculate the logical 'or'
        self.neuralor = {'Input1' : ['HiddenNeuron1'],
                         'Input2' : ['HiddenNeuron2'],
                         'HiddenNeuron1' : ['OutputNeuron'],
                         'HiddenNeuron2' : ['OutputNeuron']}
        # Adapted from Blondie 24 figure 32 pg 168 -- partial graph of inititial Blondie neuralnet
        self.blondie0 = {'InputNeuron1' : ['HiddenLayer1Neuron1', 'HiddenLayer1Neuron40', 'OutputNeuron'],
                         'InputNeuron2' : ['HiddenLayer1Neuron1', 'HiddenLayer1Neuron40', 'OutputNeuron'],
                         'HiddenLayer1Neuron1' : ['HiddenLayer2Neuron1', 'HiddenLayer2Neuron10'],
                         'HiddenLayer1Neuron40' : ['HiddenLayer2Neuron1', 'HiddenLayer2Neuron10'],
                         'HiddenLayer2Neuron1' : ['OutputNeuron'],
                         'HiddenLayer2Neuron10' : ['OutputNeuron']
                         }
        # Adapted from Blondie 24, figure 11, pg 60 -- cartoon version of a genetic system
        self.cartoongenome = {'ComplexStar': ['f'],
                              'Gene1': ['Triangle'],
                              'Gene2': ['Square'],
                              'Gene3': ['Pentagon'],
                              'Gene4': ['Hexagon'],
                              'Gene5': ['Octagon'],
                              'Gene6': ['SimpleStar'],
                              'Gene7': ['InvertedTriangle'],
                              'Gene8': ['ComplexStar'],
                              'Hexagon': ['e', 'h'],
                              'InvertedTriangle': ['c', 'g', 'h'],
                              'Octagon': ['d'],
                              'Pentagon': ['a', 'b'],
                              'SimpleStar': ['e', 'f'],
                              'Square': ['c', 'e'],
                              'Triangle': ['b', 'd', 'f']
                              }
    def test_001_NormalCase(self):
        """ findRootsLeaves_001_Normal Case:  Tests cases where Roots/Leaves of a Graph found """
        actualoutput_perceptron = xayacore.findRootsLeaves(self.perceptron)
        sortedoutput_perceptron = {}
        for key in actualoutput_perceptron:
            listvalue_perceptron = actualoutput_perceptron[key]
            listvalue_perceptron.sort()
            sortedoutput_perceptron[key] = listvalue_perceptron
        self.assertEqual(sortedoutput_perceptron,
                         {'Interior': ['HiddenNeuron1', 'HiddenNeuron2'],
                          'AllNodes': ['HiddenNeuron1', 'HiddenNeuron2', 'InputNeuron1', 'InputNeuron2', 'InputNeuron3', 'OutputNeuron1', 'OutputNeuron2'],
                          'Leaves': ['OutputNeuron1', 'OutputNeuron2'],
                          'Roots': ['InputNeuron1', 'InputNeuron2', 'InputNeuron3']})
        actualoutput_neuralor = xayacore.findRootsLeaves(self.neuralor)
        sortedoutput_neuralor = {}
        for key in actualoutput_neuralor:
            listvalue_neuralor = actualoutput_neuralor[key]
            listvalue_neuralor.sort()
            sortedoutput_neuralor[key] = listvalue_neuralor
        self.assertEqual(sortedoutput_neuralor,
                        {'Interior': ['HiddenNeuron1', 'HiddenNeuron2'],
                         'AllNodes': ['HiddenNeuron1', 'HiddenNeuron2',
                                      'Input1', 'Input2', 
                                      'OutputNeuron', ],
                         'Leaves': ['OutputNeuron'],
                         'Roots': ['Input1', 'Input2']})

class xayacore_reverseGraph(unittest.TestCase):
    def setUp(self):
        # forwardGraph1 -- has no arcless nodes
        self.forwardGraph1 = {'a':[1,2,3,4,5], 'b': [6,7,8,9], 5: [8,9]}
        # forewardGraph2 -- has an arcless node 'c' and a terminal node explictly specified, 9
        self.forewardGraph2 = {'a':[1,2,3,4,5], 'b': [6,7,8,9], 5: [8,9], 9: [], 'c' : []}
        # reverseGraph1 -- reverse of forwardGraph1
        self.reverseGraph1 = {1: ['a'], 2: ['a'], 3: ['a'], 4: ['a'], 5: ['a'], 6: ['b'], 7: ['b'], 8: ['b', 5], 9: ['b', 5]}
        # reverseGraph2 -- reverse of forwardGraph2
        self.reverseGraph2 = {1: ['a'], 2: ['a'], 3: ['a'], 4: ['a'], 5: ['a'], 6: ['b'], 7: ['b'], 8: ['b', 5], 9: ['b', 5], 'c': []}
        # self.reforwardGraph1 -- reverse of reverseGraph1 -- should give original forwardGraph1
        self.reforwardGraph1 = {'a':[1,2,3,4,5], 'b': [6,7,8,9], 5: [8,9]}
        self.reforwardGraph2 = {1: ['a'], 2: ['a'], 3: ['a'], 4: ['a'], 5: ['a'], 6: ['b'], 7: ['b'], 8: ['b', 5], 9: ['b', 5], 'c': []}
        
    #def test_001_NormalCase(self):
        

    
if __name__ == '__main__':
    unittest.main()