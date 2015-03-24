#!/usr/bin/env python


"""
BeginDate:20040902
CurrentRevisionDate:20041130
Development Version : core 001
Release Version: pre-release

Author(s): Mishtu Banerjee, Tyler Mitchell
Contact: mishtu@harmeny.com

Copyright: The Authors
License: Distributed under MIT License
    [http://opensource.org/licenses/mit-license.html]
    
Environment: Programmed and tested under Python 2.3.3 on Windows 2000.
    Database Access: Sqlite and  Psycopg and Postgres 7.4
    
Dependencies:
    Python Interpreter and base libraries.
    Sqlite [website] Main Focus
    Psycopg [website]
    Postgres [website] test X
    MS Access [website]
    


==============================================
XAYAdb_001 A Language for Thinking with Data
==============================================

Steps to Bring LifeLine Like Functionality into XAYAdb

1. Given a "Schema" as a graph -- generate an SQL string to display all column
    in all tables in the path
        Pattern: Select * From Table1, Table2, .... where Table1Pkey=Table2Fkey,
        Table2Pkey = Table3FKey .....
            Assumptions: All tables on the path have:
            Primary key as TableName_ID, and that any child table, has it's
            Parents primary key.
            
2. Given a "Schema" and "Measures", "Columns to Display" as graphs -- generate an
    SQL string that displays only the selected measures.
        Assume: Primary Keys.
        
3. Given a "Schema", "Measures" and "Keys" as graphs -- generate an SQL string
    that displays data, using the named keys. Question: Restrict to single key.
    
4. Wrap in a DB access module.

5. Given a Schema, A Measures, A Keys, Measure/Operator/Value -- generate an SQL
    string that displays data using named keys, and restricts data to values
    that match the operator constraints.
    
At that point, have a functional match to LifeLine's basic capabilities. 

To Do:
1. Fix up the SQL tokenizer
2. Support GROUP BY (aggregate functions)
3. Allow specifying join types, via a JOINS list.


"""
import xayacore
import xayastats
import re

# To allow the code to use built-in set fns in Python 2.4 or the sets module in Python 2.3
try :
    set
except NameError:
    from sets import Set as set

# ---------- Error Handling ----------

class xayadbSQLError(Exception):
    def __init__(self, arg = None):
        self.arg = arg
    def __str__(self):
        return str(self.arg)

  



geomGraph = {'FC':  {
                                    'SpatialColumn': 'TheGeom',
                                    'SpatialType': 'Polygon'},
                         'VRI' : {
                                    'SpatialColumn': 'VRIGeom',
                                    'SpatialType': 'Polygon'}
                                                                             }
             
# Spatial Predicates return boolean -- True/False
allowableSpatialPredicatesList = ['intersects', 'touches',  'disjoint',
        'equals', 'touches', 'crosses', 'within', 'overlaps' , 'contains', ]
# Spatial Functions Return a Numerical Value
allowableSpatialFunctionsList = ['distance']
# These Spatial Predicates define joins -- but do not create new geometries.
spatialJoinsGraph = { 'intersects': ['FC', 'VRI'], 'distances':['FC', 'VRI' , '=', 0]}
allowableOperatorsList = ['=', '<>', '>=', '<=', '<', '>']
allowableAggregatesList = ['sum','avg','stdev','min','max']


# ---------- SQL Generator ----------

def genSQL(pathList = [ ], columnsGraph= {}, expressionsList = [], primarykeysGraph={},
           constraintsList = [ ], geomGraph= {}, spatialJoinsGraph={}, aggregateFunctionsList = [] ):
    """
    Generate an SQL string to query db based on knowing the pathList of tables
    to join, the columnsGraph" of data to view, the primarykeysGraph
    defining unique rows of data and th contraintsList which defines how
    you wish to filter your data

    """
    sqlList = [ ]
    if (columnsGraph == {}) and (expressionsList == []):
        sqlList.append('SELECT * FROM '  + " , ".join(_findDistinctTableNames(pathList, geomGraph) )+ " ")
    else:
        selClauseList = _selectClause(columnsGraph, aggregateFunctionsList) + expressionsList
        sqlList.append('SELECT  ' +  ",".join(selClauseList)+ ' FROM ' + " , ".join(_findDistinctTableNames(pathList, geomGraph)) + "  ")
    if primarykeysGraph == {} :
        tempGraph = {}
        for entity in pathList:
            tempGraph[entity] = [entity + 'ID']
        primarykeysGraph = tempGraph
        #    sqlString = " ".join(sqlList) + whereJoinsClause(pathList=pathList, primarykeysGraph=primarykeysGraph)
    whereJoins = _whereJoinsClause(pathList=pathList, primarykeysGraph=primarykeysGraph)
    whereConstraints = _whereConstraintsClause(constraintsList = constraintsList)
    whereSpatialConstraints = _whereSpatialJoinsClause(geomGraph, spatialJoinsGraph)
    if (whereJoins == "" )and (whereConstraints == "") and (whereSpatialConstraints == ""):
        whereClause = ""
    elif (whereJoins <> "" )and (whereConstraints <> "") and (whereSpatialConstraints <> ""):
        whereClause = "WHERE " + whereJoins + " AND " + whereConstraints +  " AND " + whereSpatialConstraints
    elif (whereJoins == "" )and (whereConstraints <> "") and (whereSpatialConstraints <> ""):
        whereClause = "WHERE " + whereConstraints +  " AND " + whereSpatialConstraints
    elif (whereJoins <> "" )and (whereConstraints == "") and (whereSpatialConstraints <> ""):
        whereClause = "WHERE " + whereJoins + " AND " + whereSpatialConstraints
    elif (whereJoins <> "" )and (whereConstraints <> "") and (whereSpatialConstraints == ""):
        whereClause = "WHERE " + whereJoins + " AND " + whereConstraints
    elif (whereJoins == "" )and (whereConstraints == "") and (whereSpatialConstraints <> ""):
        whereClause = "WHERE " + whereSpatialConstraints
    elif (whereJoins == "" )and (whereConstraints <> "") and (whereSpatialConstraints == ""):
        whereClause = "WHERE " + whereConstraints
    elif (whereJoins <> "" )and (whereConstraints == "") and (whereSpatialConstraints == ""):
        whereClause = "WHERE " + whereJoins
    groupByClause = _groupByClause(columnsGraph, aggregateFunctionsList)
    sqlString = " ".join(sqlList) + whereClause + groupByClause
    return sqlString

def _selectClause(columnsGraph= {}, aggregateFunctionsList = []):
    """
    Generate an SQL sub-string representing the
    data you wish to view based on the columnsGraph of tables and fields

    """
    aggregateColumnsGraph = {}
    for graph in aggregateFunctionsList:
        aggregateColumnsGraph[graph['TableName'] + "." + graph['ColumnName']] = graph['Aggregate']
    columnsList = []
    for node in columnsGraph.keys():
        for child in columnsGraph[node]:
            col = str(node + '.' + child)
            if col in aggregateColumnsGraph.keys():
                col = str(aggregateColumnsGraph[col]) + "(" + col + ")"
            columnsList.append(col)
    return columnsList

def _whereJoinsClause(pathList=[ ], primarykeysGraph ={ }):
    """
    Generate an SQL sub-string representing the join conditions across tables
    based on the primarykeysGraph that specifies unique data in each table and
    defines the foreign keys used to join across tables

    """
    sqlList = [ ]
    if len(pathList) >= 2:
        lastNode=pathList[0]
        for entity in pathList[1:] :
            for key in primarykeysGraph[lastNode]:
                sqlList.append(lastNode + '.' + key + '=' + entity  +  '.' + key)
                sqlList.append('AND')
            lastNode = entity
        if sqlList[-1] == 'AND' :
            sqlList = sqlList[0 : -1]
    sqlString = " ".join(sqlList)
    return sqlString


def _whereConstraintsClause(constraintsList = []):
    """
    Defines an SQL sub-string restricting rows of data returned.
    Assumes a constraintsList of the form [dict1, dict2, dict3 ...]
    where each item in the list is a dictionary whose keys are: TableName,
    ColumnName,Operator,Values with a single string value for
    TableName, ColumnName, and Operator; and with a list of values
    for Values
    
    """    
    allowedConstraintsGraph = {'=' :['='],
                               '>': ['>'],
                               '<': ['<'],
                               '<>' : ['<>'],
                               '<=': ['<='],
                               '>=' : ['>=']}
    # Check 2 -- Operators are allowed Constraints
    # Check3 -- Values is a list
    # Check 1 -- Our  dictionaries are proper format.
    # Check 0: Constraints is a list; Every item in list is a dictionary
    #Check4:if Operator not in ['<>', '='] then list must be of length 1
    # Implement checks via raising Exceptions -- create specific exception handlers
    if type(constraintsList) <> type([]):
        return 'You must enter a list of constraints'
    newValueList = []
    for items in constraintsList:
        for dict in constraintsList:
            strtblName = str(dict['TableName'] + '.' + dict['ColumnName'])
            strOperator = str(dict['Operator'])
            newValueList.append('(')
            for item in dict['Values']:
                if xayastats.testTypes(item) in ['TEXT','CATEGORICAL']:
                    quotedItem = "'" + str(item) + "'"
                else:
                    quotedItem = str(item)
                newValueList.append('(' + strtblName + strOperator + quotedItem + ')')
                newValueList.append('OR')
            if newValueList[-1] == 'OR':
                newValueList = newValueList[:-1]
            newValueList.append(')')
            newValueList.append('AND')
    if (newValueList <> []) and (newValueList[-1] == 'AND') :
        newValueList = newValueList[:-1]
    return ' '.join(newValueList)
            
def whereJoinsClause2(pathList=[ ], primarykeysGraph ={ }, joinsList = [ ]):
    return 'Under Construction'

# ---------- Spatial Functions

def _whereSpatialJoinsClause(geomGraph= {}, spatialJoinsGraph={}):
    """ Defines spatial component of a join via data in geomGraph (defines geometry column  and geometry type
    in a table   and  spatialJoinsGraph which describes pair-wise spatial join operations
    """
    
    if spatialJoinsGraph == {}: return ""
    if geomGraph == {}:  raise xayadbSQLError( "Need A geomGraph")
    for key in spatialJoinsGraph:
        if (key.lower()  not in allowableSpatialPredicatesList) and (key.lower() not in allowableSpatialFunctionsList): raise xayadbSQLError("Inadmissable Spatial Operator")
    spatialwhereClause = ''
    for joinkey in spatialJoinsGraph:
        leftItem = spatialJoinsGraph[joinkey][0]
        rightItem = spatialJoinsGraph[joinkey][1]
        leftEntity = leftItem + "." + geomGraph[leftItem]['SpatialColumn']
        rightEntity = rightItem + "." + geomGraph[rightItem]['SpatialColumn']
        if joinkey.lower() in allowableSpatialPredicatesList:
            spatialwhereClause = spatialwhereClause + leftEntity + ' && ' + rightEntity + ' AND ' + joinkey.upper() + '(' + leftEntity + ', ' + rightEntity + ') AND '
        else :
            operator = spatialJoinsGraph[joinkey][2]
            value = spatialJoinsGraph[joinkey][3]
            spatialwhereClause = spatialwhereClause  + leftEntity + ' && ' + rightEntity + ' AND ' + joinkey.upper() + '(' + leftEntity + ', ' + rightEntity + ') '+ operator + " "  + str(value) + ' AND '
            
    if spatialwhereClause != '':
        spatialwhereClause = spatialwhereClause[:-5]
    return  spatialwhereClause

def _findDistinctTableNames(pathList = [], geomGraph = {}):
    geomGraphkeys = geomGraph.keys()
    pathsset = set(pathList)
    geomset = set(geomGraphkeys)
    unionset = pathsset.union(geomset)
    return list(unionset)

def _groupByClause(columnsGraph = {}, aggregateFunctionsList = []):
    if aggregateFunctionsList == []: return ""
    columnsList = []
    for table in columnsGraph.keys():
        for column in columnsGraph[table]:
            columnsList.append(table + "." + column)
    aggregateColumnsList = []
    for graph in aggregateFunctionsList:
        if graph['Aggregate'] not in allowableAggregatesList:
            raise xayadbSQLError("Not an allowable aggregate function")
        aggregateColumnsList.append(graph['TableName'] + "." + graph['ColumnName'])
    columnsSet = set(columnsList)
    aggregateColumnsSet = set(aggregateColumnsList)
    if aggregateColumnsSet.intersection(columnsSet) != aggregateColumnsSet:
        raise xayadbSQLError("Aggregate column(s) do not appear in columnsGraph")
    groupBySet = columnsSet.difference(aggregateColumnsSet)
    groupByClause = ""
    for column in groupBySet:
        groupByClause = groupByClause + column + ","
    if groupByClause != "":
        groupByClause = " GROUP BY " + groupByClause[:-1]
    return groupByClause
    
def tokenizeSQLString(SQLString = ''):
    """
    Extremely simple tokenizer. Here are a few things it cannot handle properly:
    - quoted strings (e.g. 'Prince George' ==> ["'Prince", "George'"] )
    - arithmetic operators (e.g. '(area)/10000' ==> ["(", "area", ")", "/10000"] )
    - others too numerous to list here...
    """
    splitChar = '`'
    if splitChar in SQLString: raise xayadbSQLError("SQLString contains a '" + splitChar + "'")
    workString = re.sub('\s+', ' ', SQLString) # replace all instances of whitespace with a single space
    workString = re.sub('\s*,\s*', splitChar + ',' + splitChar, workString) # replace all instances of ',' with splitChar + ',' + splitChar
    workString = re.sub('\s*\(\s*', splitChar + '(' + splitChar, workString) # replace all instances of '(' with splitChar + '(' + splitChar
    workString = re.sub('\s*\)\s*', splitChar + ')' + splitChar, workString) # replace all instances of ')' with splitChar + ')' + splitChar
    workString = re.sub(' ', splitChar, workString) # replace ' 's with splitChar's
    workString = workString.strip(splitChar)  # remove leading and trailing splitChar's
    workList = workString.split(splitChar)  # split on splitChar
    return workList




    



    

  