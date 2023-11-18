"""
Translation of ShellUtilities.java to python
original file: https://github.com/pfred/pfred-rest-service/blob/python3-Ensembl/src/main/java/org/pfred/rest/service/ShellUtilities.java

@author: Steven Qiu<mumingpo@gmail.com>
"""

import os
import logging
from pathlib import Path
from shutil import copy, rmtree
from subprocess import run

logger = logging.getLogger("pfred.shell_utilities")

def get_run_dir():
    try:
        return os.environ["RUN_DIR"]
    except KeyError as e:
        raise RuntimeError("Environmental variable RUN_DIR is not set.") from e

def get_scripts_dir():
    try:
        return os.environ["SCRIPTS_DIR"]
    except KeyError as e:
        raise RuntimeError("Environmental variable SCRIPTS_DIR is not set.") from e

def run_command_through_shell(command: str, directory: str):
    # env = os.environ.copy()
    # env["PATH"] = "{}:{}".format(get_scripts_dir(), env["PATH"])

    logger.info("Running Shell Command: {}".format(command))
    try:
        run(
          command,
          cwd=directory,
        #   env=env,
          shell=True,
          executable="/bin/bash",
        )
    except Exception as e:
        logger.error("Error executing command line in bash shell", exc_info=e)

        return False

    return True

def read_file_as_string(file_path: str):
    with open(file_path, "rt") as f:
        s = f.read()
    
    return s

def save_string_as_file(file_path: str, contents: str):
    try:
        with open(file_path, "wt") as f:
            f.write(contents)
    except IOError as e:
        logger.error("Error saving string as file", exc_info=e)

def copy_file(file_path: str, target_directory: str):
    try:
        copy(src=file_path, dst=target_directory)
    except IOError as e:
        logger.error(
            "Error copying file from {} to {}".format(file_path, target_directory),
            exc_info=e,
        )

def prepare_run_dir(run_name: str):
    run_directory = get_run_dir()
    full_run_directory = Path(os.path.join(run_directory, run_name))
    if (not full_run_directory.is_dir()):
        full_run_directory.mkdir()
    
    return full_run_directory

def remove_dir(dir_path: str):
    logger.info("Removing run directory: {}".format(dir_path))
    try:
        rmtree(dir_path)
    # FIXME: I don't think it would result in an IOError
    # but I don't know what type of error would be raised
    except Exception as e:
        logger.error("Error removing directory: {}".format(dir_path), exc_info=e)

        return False
    
    return True
