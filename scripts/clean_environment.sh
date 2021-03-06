#!/usr/bin/env bash

# Function 'clean_environment' can be used to clean the developing environment.
# From the command line: . ./clean_environment.sh && cd .. && clean_environment

export ALREADY_SOURCED_CLEAN_ENVIRONMENT

if [ -z "${ALREADY_SOURCED_CLEAN_ENVIRONMENT}" ]
then
    clean_environment()
    {
        printf "%sCleaning developing environment at '%s'...%s" "${YELLOW}" "${PWD}" "${NORMAL}"
        find . -type f -name "*.py[co]" -delete
        find . -type d -name "__pycache__" -delete
        find . -type f -name ".coverage" -delete
        rm -rf ands.egg-info
        rm -rf venv
        printf "%s done.%s\n" "${GREEN}" "${NORMAL}"
    }

    . ./_source_script.sh
    _source_script scripts colors

    ALREADY_SOURCED_CLEAN_ENVIRONMENT="true"
fi