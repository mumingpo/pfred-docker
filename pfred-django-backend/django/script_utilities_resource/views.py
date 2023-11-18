"""
Translation of ScriptUtilitiesResource.java to python
original file: https://github.com/pfred/pfred-rest-service/blob/python3-Ensembl/src/main/java/org/pfred/rest/service/ScriptUtilitiesResource.java

@author: Steven Qiu<mumingpo@gmail.com>
"""

# FIXME: !important security audit for deletion operations (ie: RunDirectory=%2F or something)
# FIXME: REST methods
# FIXME: status code

import os
import logging
from pathlib import Path

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET

import shell_utilities

logger = logging.getLogger('pfred.script_utilities_resource.views')

def success_response(content:str):
    return HttpResponse(content, status=200, content_type="text/plain")
def failure_response(content:str):
    logging.error(content)
    return HttpResponse(content, status=400, content_type="text/plain")

@require_GET
def get_orthologs(request: HttpRequest):
    try:
        ensebl_id = request.GET["enseblID"]
        run_name = request.GET["RunDirectory"]
        requested_species = request.GET["RequestedSpecies"]
        species = request.GET["Species"]

    except KeyError as e:
        return failure_response("Malformed request for get_orthologs: {}".format(e))

    full_run_directory = shell_utilities.prepare_run_dir(run_name)
    command = f"getOrthologs.sh {ensebl_id} {species} {requested_species}"
    output_file_path = os.path.join(full_run_directory, "seqAnnotation.csv")

    success = shell_utilities.run_command_through_shell(command, full_run_directory)

    if (success):
        logger.info("Shell command run successfully")

        try:
            result = shell_utilities.read_file_as_string(output_file_path)
            return success_response(result)
        except FileNotFoundError as e:
            return failure_response("seqAnnotation.csv not found after get_orthologs")
        except Exception as e:
            return failure_response("Error occured while delivering seqAnnotation.csv: {}".format(e))

    return failure_response("Shell command run failed during get_orthologs")

@require_GET
def enumerate_first(request: HttpRequest):
    try:
        secondary_transcript_ids = request.GET["SecondaryTranscriptIDs"]
        run_name = request.GET["RunDirectory"]
        primary_transcript_id = request.GET["PrimaryTranscriptID"]
        oligo_len = request.GET["oligoLen"]

    except KeyError as e:
        return failure_response("Malformed request for enumerate_first: {}".format(e))
    
    full_run_directory = shell_utilities.prepare_run_dir(run_name)
    command = f"Enumeration.sh {secondary_transcript_ids} {primary_transcript_id} {oligo_len}"
    output_file_path = os.path.join(full_run_directory, "EnumerationResult.csv")

    success = shell_utilities.run_command_through_shell(command, full_run_directory)

    if (success):
        logger.info("Shell command run successfully")
        try:
            results = shell_utilities.read_file_as_string(output_file_path)
            return success_response(results)
        except FileNotFoundError as e:
            return failure_response("EnumerationResult.csv not found after enumerate_first")
        except Exception as e:
            return failure_response("Error occured while delivering EnumerationResult.csv")
        
    return failure_response("Shell command run failed during enumerate_first")

@require_GET
def enumerate_second(request: HttpRequest):
    try:
        run_name = request.GET["RunDirectory"]
        
    except KeyError as e:
        return failure_response("Malformed request for enumerate_second: {}".format(e))
    
    full_run_directory = shell_utilities.prepare_run_dir(run_name)
    output_file_path = os.path.join(full_run_directory, "sequence.fa")

    try:
        sequence_file = Path(output_file_path)
        if (not sequence_file.is_file()):
            return failure_response("sequence.fa does not exist for enumerate_second")
        if (sequence_file.stat().st_size == 0):
             return failure_response("sequence.fa is empty for enumerate_second")
        
        results = shell_utilities.read_file_as_string(output_file_path)
        return success_response(results)
    
    except Exception as e:
        return failure_response("Error occured while delivering sequence.fa: {}".format(e))

@require_GET
def clean_run_dir(request: HttpRequest):
    try:
        run_name = request.GET["RunDirectory"]
        
    except KeyError as e:
        return failure_response("Malformed request for clean_run_dir: {}".format(e))
    
    full_run_directory = os.path.join(shell_utilities.get_run_dir(), run_name)

    try:
        success = shell_utilities.remove_dir(full_run_directory)

        if (success):
            result = "Run directory removed"
            return success_response(result)

    except Exception as e:
        return failure_response("Unable to clean: {}".format(e))
    
    return failure_response("Unable to remove run directory during clean")

@require_GET
def append_to_file(request: HttpRequest):
    try:
        file_name = request.GET["FileName"]
        text = request.GET["Text"]
        run_name = request.GET["RunDirectory"]
        
    except KeyError as e:
        return failure_response("Malformed request for append_to_file: {}".format(e))

    full_run_directory = shell_utilities.prepare_run_dir(run_name)
    output_file_path = os.path.join(full_run_directory, file_name)

    try:
        with open(output_file_path, "at") as f:
            f.write(text)
        
        return success_response("OK")
    except Exception as e:
        return failure_response("Unable to append to file: {}".format(e))
