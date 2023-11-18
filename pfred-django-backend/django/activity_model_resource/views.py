"""
Translation of ActivityModelResource.java to python
original file: https://github.com/pfred/pfred-rest-service/blob/python3-Ensembl/src/main/java/org/pfred/rest/service/ActivityModelResource.java

@author: Steven Qiu<mumingpo@gmail.com>
"""

import logging
import os

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST

import shell_utilities

def success_response(content:str):
    return HttpResponse(content, status=200, content_type="text/plain")
def failure_response(content:str):
    logging.error(content)
    return HttpResponse(content, status=400, content_type="text/plain")

logger = logging.getLogger("pfred.activity_model_resource.views")

@require_POST
def run_sirna_activity_model(request: HttpRequest):
    try:
        # weird thing withd django, even if method is POST
        # query params are still in GET
        primary_id = request.GET["PrimaryID"]
        run_name = request.GET["RunDirectory"]

    except KeyError as e:
        return failure_response("Malformed request for run_sirna_activity_model: {}".format(e))

    full_run_directory = shell_utilities.prepare_run_dir(run_name)
    command = f"getSeqGivenTrans.sh {primary_id}"
    logger.info(command)
    success = shell_utilities.run_command_through_shell(command, full_run_directory)

    if (not success):
        return failure_response("run_sirna_activity_model failed during getSeqGivenTrans.sh")
    
    logger.info("getSeqGivenTrans.sh run successfully")

    shell_utilities.copy_file(
        file_path=os.path.join(shell_utilities.get_scripts_dir(), "siRNA_2431seq_modelBuilding.csv"),
        target_directory=full_run_directory,
    )

    command = "siRNAActivityModel.sh"
    output_file_path = os.path.join(full_run_directory, "siRNAActivityModelResult.csv")
    success = shell_utilities.run_command_through_shell(command, full_run_directory)

    if (not success):
        return failure_response("run_sirna_activity_model failed during siRNAActivityModel.sh")
    
    logger.info("siRNAActivityModel.sh run successfully")
    try:
        result = shell_utilities.read_file_as_string(output_file_path)
        return success_response(result)

    except FileNotFoundError as e:
        return failure_response("siRNAActivityModelResult.csv not found after run_sirna_activity_model")
    except Exception as e:
        return failure_response("Error occured while delivering siRNAActivityModelResult.csv: {}".format(e))

@require_POST
def run_aso_activity_model(request: HttpRequest):
    try:
        # weird thing withd django, even if method is POST
        # query params are still in GET
        primary_id = request.GET["PrimaryID"]
        run_name = request.GET["RunDirectory"]
        # oligo_length = request.GET["OligoLength"]

    except KeyError as e:
        return failure_response("Malformed request for run_aso_activity_model: {}".format(e))

    full_run_directory = shell_utilities.prepare_run_dir(run_name)
    command = f"getSeqGivenTrans.sh {primary_id}"
    logger.info(command)
    success = shell_utilities.run_command_through_shell(command, full_run_directory)

    if (not success):
        return failure_response("run_aso_activity_model failed during getSeqGivenTrans.sh")
    
    logger.info("getSeqGivenTrans.sh run successfully")

    scripts_dir = shell_utilities.get_scripts_dir()
    shell_utilities.copy_file(
        file_path=os.path.join(scripts_dir, "input_15_21_100_1000_12.txt"),
        target_directory=full_run_directory,
    )
    shell_utilities.copy_file(
        file_path=os.path.join(scripts_dir, "AOBase_542seq_cleaned_modelBuilding_Jan2009_15_21_noOutliers.csv"),
        target_directory=full_run_directory,
    )

    command = "ASOActivityModel.sh"
    output_file_path = os.path.join(full_run_directory, "ASOActivityModelResult.csv")
    success = shell_utilities.run_command_through_shell(command, full_run_directory)

    if (not success):
        return failure_response("run_aso_activity_model failed during ASOActivityModel.sh")
    
    try:
        result = shell_utilities.read_file_as_string(output_file_path)
        return success_response(result)

    except FileNotFoundError as e:
        return failure_response("ASOActivityModelResult.csv not found after run_aso_activity_model")
    except Exception as e:
        return failure_response("Error occured while delivering ASOActivityModelResult.csv: {}".format(e))
    