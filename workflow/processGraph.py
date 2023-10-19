from estimationnode import EstimationNode
from openeooperation import *
from constants import constants
import copy
##from constants.constants import *

class ProcessNode :
    constants.UNDEFINED = 0
    OPERATION = 1
    JUNCTION = 2
    CONDITION = 3

    def __init__(self, parentProcessGraph, nodeDict, nodeName):
        self.nodeName = nodeName ## just for easy identification; doesnt play a role on this level
        self.parentProcessGraph = parentProcessGraph
        for key, pValue in nodeDict.items():
            if key == 'process_id':
                self.process_id = pValue
            elif key == 'arguments':
                self.localArguments = {}
                for key, value in pValue.items():
                    self.localArguments[key] = { 'base' : value, 'resolved' : None}

            elif key == 'description':
                self.description = pValue
            elif key == 'result':
                self.result = pValue
               
            self.nodeType = ProcessNode.OPERATION 
            self.nodeValue = None

class ProcessGraph(OpenEoOperation):

    def __init__(self, source_graph, arguments, getOperation):
        self.processGraph = {}
        self.outputNodes = []
        self.sourceGraph = source_graph
        self.processArguments = arguments
        self.localArguments = {}
        self.getOperation = getOperation
        print(self.getOperation)
        self.startNode = None
        for processKey,processValues in source_graph.items():
            grNode = ProcessNode(self, processValues, processKey)
            self.processGraph[processKey] = grNode
            
        self.determineOutputNodes(self.processGraph)

    def determineOutputNodes(self, nodes):
        for node in nodes.items():
            if hasattr(node[1], 'result'):
                self.outputNodes.append(node)

    def validateNode(self, node):
        errors = []
        for arg in node.arguments.items():
                if ( node.argumentValues[arg[0]] == None): # ninput from other node
                    fromNodeId = arg[1]['from_node']
                    backNode = self.id2Node(fromNodeId)
                    errors = errors + self.validateNode(backNode[1])
                   
        processObj = self.getOperation(node.process_id)
        if processObj == None:
             errors.append("missing \'operation\' " + node.process_id  )

        return errors             

    def validateGraph(self):
            errors = []
            for node in self.outputNodes:
                errors = errors + self.validateNode(node[1])
            return errors                
                   
    def prepare(self, arguments):
        return ""
    
    def estimate(self):
        try:
            for node in self.outputNodes:
                self.startNode = EstimationNode(node,self)
                return self.startNode.estimate()

        except Exception as ex:
            return createOutput(False, str(ex), constants.DTERROR)

    def run(self,job_id, toServer, fromServer ):
        try:
            for key, processNode in self.outputNodes:
                self.startNode = NodeExecution(processNode,self)
                self.startNode.run(job_id, toServer, fromServer)
                return self.startNode.outputInfo
        except Exception as ex:
            return createOutput(False, str(ex), constants.DTERROR)
        
    def stop(self):
        if self.startNode != None:
            self.startNode.stop()

    def processGraph(self):
        return self.sourceGraph
    

    def id2node(self, id):
        for node in self.processGraph.items():
            if node[0] == id:
                return node
        return None            

    def determineOutputNodes(self, nodes):
        for node in nodes.items():
            if hasattr(node[1], 'result'):
                self.outputNodes.append(node)   

class NodeExecution :

    def __init__(self, processNode, processGraph):
        self.processNode = processNode
        self.processGraph = processGraph
        self.outputInfo = None
        self.indirectKeys = ['from_parameter', 'from_node', 'reducer']

    def run(self, job_id, toServer, fromServer):
        args = self.processNode.localArguments
        for key, parmDef in args.items():
            if parmDef['resolved'] == None:
                definition = parmDef['base']
                if isinstance(definition, dict):
                   for item in definition.items():
                        if item[0] in self.indirectKeys:
                            resolvedValue = self.resolveNode(job_id, toServer, fromServer, item)
                        else:            
                            resolvedValue = self.resolveNode(job_id, toServer, fromServer, (key, definition)) 
                else:
                    resolvedValue = self.resolveNode(job_id, toServer, fromServer, (key, definition))                        
                args[key]['resolved'] = resolvedValue

        processObj = self.processGraph.getOperation(self.processNode.process_id)
        if  processObj != None:
            ##arguments = self.processNode.argumentValues
            executeObj =  copy.deepcopy(processObj)
            message = executeObj.prepare(args)
            if not executeObj.runnable:
                self.outputInfo =  createOutput(False, message, constants.DTERROR)
                return False

            try:
                self.outputInfo = executeObj.run(job_id, toServer, fromServer) 

            except Exception:
                return 'aap'

        return ''

    def resolveNode(self, job_id, toServer, fromServer, parmKeyValue):
        if 'from_node' in parmKeyValue:
            referredNodeName = parmKeyValue[1]
            referredNode = self.processGraph.id2node(referredNodeName)
            if referredNode != None:
                if referredNode[1].nodeValue == None:
                    refExecutionNode = NodeExecution(referredNode[1], self.processGraph)
                    if refExecutionNode.run(job_id, toServer, fromServer) == '':
                        referredNode[1].nodeValue = refExecutionNode.outputInfo
                        return referredNode[1].nodeValue['value']
                    return 'hmm'
        elif 'from_parameter' in parmKeyValue:
                refNode = self.processNode.parentProcessGraph.processArguments[parmKeyValue[1]]
                if refNode['resolved'] != None:
                    return refNode['resolved'] 
                return self.resolveNode(job_id, toServer, fromServer, refNode)  
        elif 'reducer' in parmKeyValue:
            pgraph = parmKeyValue[1]['process_graph']
            args = self.processNode.localArguments
            process = ProcessGraph(pgraph, args, self.processGraph.getOperation)
            return process.run(job_id, toServer, fromServer)
        else:
            return parmKeyValue[1]                                              