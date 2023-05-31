from flask_restful import Resource
from flask import make_response, jsonify, request, Response
import json
from workflow.workflow import Worklflow
from globals import globalsSingleton
from constants.constants import *
from workflow.openeoprocess import OpenEOProcess
import copy
import uuid
import sys
import traceback

class OpenEOIPResult(Resource):
    def post(self):
        request_doc = request.get_json()
        process = OpenEOProcess(request_doc)

        if process.workflow != None:
            outputInfo = process.workflow.run(False)

            if outputInfo["status"]:
                if outputInfo["datatype"] != DTRASTER:
                    res = { "job_id" : process.workflow.job_id,
                            "message" : "Process completed succesfully",
                            "data" : {
                                "type" : self.makeType(outputInfo["datatype"]),
                                "format" : outputInfo["format"],
                                "value" : outputInfo["value"]
                            }
                            }
                    return make_response(jsonify(res),200)
            elif outputInfo["datatype"] == DTRASTER:
                #dummy probably not yet correct but the this how post and images work
                with open('file_name.bin', 'rb') as file:
                    binary_data = file.read()
                    return Response(binary_data,
                                    mimetype="image/tiff",
                                    direct_passthrough=True)
                
               
            return make_response(jsonify({"job_id" : process.workflow.job_id, "job_info" :outputInfo["value"]}),404)

    def makeType(self, tp):
        if ( tp == DTNUMBER):
            return "number"
        if ( tp == DTRASTER):
            return "raster"
        return "unknown"

                        
                        

                

