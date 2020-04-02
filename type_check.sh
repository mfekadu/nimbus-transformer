#!/bin/bash

# e.g., "/Users/{USERNAME}/.local/share/virtualenvs/nimbus-transformer-03ms5r62"
pipenv_location=$(pipenv --venv)

# e.g., "Python 3.6.8"
pipenv_python_version=$(pipenv run python --version)

# echo $pipenv_python_version

python_version_folder=$(
    echo $pipenv_python_version |    # Python 3.6.8 >>>
        tr '[:upper:]' '[:lower:]' | # python 3.6.8 >>>
        tr -d "[:space:]" |          # python3.6.8  >>>
        grep -o "\w*\d\.\d"          # python3.6
)

# echo $python_version_folder

site_packages_path="$pipenv_location/lib/$python_version_folder/site-packages/"

echo $site_packages_path
echo
echo

pyre --search-path \
    $site_packages_path \
    --source-directory \
    . \
    check
