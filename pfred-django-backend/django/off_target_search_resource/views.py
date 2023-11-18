"""
Translation of OffTargetSearchResource.java to python
original file: https://github.com/pfred/pfred-rest-service/blob/python3-Ensembl/src/main/java/org/pfred/rest/service/OffTargetSearchResource.java

@author: Steven Qiu<mumingpo@gmail.com>
"""

import logging
import os

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET

import shell_utilities

logger = logging.getLogger('pfred.off_target_search_resource.views')

def success_response(content:str):
    return HttpResponse(content, status=200, content_type="text/plain")
def failure_response(content:str):
    logging.error(content)
    return HttpResponse(content, status=400, content_type="text/plain")

@require_GET
def run_sirna_off_target_search(request: HttpRequest):
    try:
        species = request.GET["Species"]
        run_name = request.GET["RunDirectory"]
        ids = request.GET["IDs"]
        miss_matches = request.GET["missMatches"]

    except KeyError as e:
        return failure_response("Malformed request for run_sirna_off_target_search: {}".format(e))
    
    full_run_directory = shell_utilities.prepare_run_dir(run_name)
    command = f"siRNAOffTargetSearch.sh {species} {ids} {miss_matches}"
    output_file_path = os.path.join(full_run_directory, "siRNAOffTargetSearchResult.csv")
    success = False

    logger.info(species)

    if (species == "paco"):
        logger.info("Shell command Avoided, skipping...")
        success = True
    else:
        success = shell_utilities.run_command_through_shell(command, full_run_directory)

    if (not success):
        return failure_response("run_sirna_off_target_search failed during siRNAOffTargetSearch.sh")

    logger.info("siRNAOffTargetSearch.sh run successfully")
    try:
        result = shell_utilities.read_file_as_string(output_file_path)
        return success_response(result)
    except FileNotFoundError as e:
        return failure_response("siRNAOffTargetSearchResult.csv not found after run_sirna_off_target_search")
    except Exception as e:
        return failure_response("Error occured while delivering siRNAOffTargetSearchResult.csv: {}".format(e))

@require_GET
def run_aso_off_target_search(request: HttpRequest):
    try:
        species = request.GET["Species"]
        run_name = request.GET["RunDirectory"]
        ids = request.GET["IDs"]
        miss_matches = request.GET["missMatches"]

    except KeyError as e:
        return failure_response("Malformed request for run_aso_off_target_search: {}".format(e))

    full_run_directory = shell_utilities.prepare_run_dir(run_name)
    command = f"ASOOffTargetSearch.sh {species} {ids} {miss_matches}"
    output_file_path = os.path.join(full_run_directory, "ASOOffTargetSearchResult.csv")
    success = False

    logger.info(species)

    if (species == "paco"):
        logger.info("Shell command Avoided, skipping...")
        success = True
    else:
        success = shell_utilities.run_command_through_shell(command, full_run_directory)

    if (not success):
        return failure_response("run_aso_off_target_search failed during ASOOffTargetSearch.sh")

    logger.info("ASOOffTargetSearch.sh run successfully")
    try:
        result = shell_utilities.read_file_as_string(output_file_path)
        return success_response(result)
    except FileNotFoundError as e:
        return failure_response("ASOOffTargetSearchResult.csv not found after run_aso_off_target_search")
    except Exception as e:
        return failure_response("Error occured while delivering ASOOffTargetSearchResult.csv: {}".format(e))
    
@require_GET
def run_check_file(request: HttpRequest):
    try:
        file = request.GET["File"]
        run_name = request.GET["RunDirectory"]

    except KeyError as e:
        return failure_response("Malformed request for run_check_file: {}".format(e))
    
    full_run_directory = shell_utilities.prepare_run_dir(run_name)
    output_file_path = os.path.join(full_run_directory, file)

    logger.info(file)

    try:
        result = shell_utilities.read_file_as_string(output_file_path)
        return success_response(result)
    except Exception as e:
        logger.info("Failed to retrieve file", exc_info=e)
        return failure_response(str(e))
