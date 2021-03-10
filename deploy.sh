#!/bin/bash
#
# Script to build a python package and upload it to PyPi.org
#

TEST_URL='https://test.pypi.org/legacy/'

show_usage () {
    echo "Usage: ${0} [-t] TARGET " >&2
    echo "Build a package and upload it to PyPi" >&2
    echo "  -t          TARGET on PyPi 'test' || 'prod'." >&2
    exit 1
}

# If no argument provided, show help.
if [[ "${#}" -lt 1 ]]; then
  show_usage
  exit 1
fi

# Check the arguments.
while getopts t OPTION
do
  case ${OPTION} in
    t) PRODUCTION='true' ;;
  esac
done

# Remove the options while leaving the remaining arguments]
shift "$(( OPTIND -1 ))"

TARGET=${@}

case ${TARGET} in
"prod")
  TARGET_REPO=""
  ;;
"test")
  TARGET_REPO="--repository-url ${TEST_URL}"
  ;;
*)
  show_usage
esac

echo "Will try to deploy to ${TARGET}"

# Check if pipenv is installed.
pipenv &> /dev/null
if [[ "${?}" -ne 0 ]]; then
  echo 'Pipenv not found. Deployment aborted.'
  exit 1
fi

# Run setup.py
pipenv run python setup.py sdist bdist_wheel
if [[ "${?}" -ne 0 ]]; then
  echo 'Build failed. Deployment aborted.'
  exit 1
fi

# Check if the build passes
pipenv run twine check dist/*
if [[ "${?}" -ne 0 ]]; then
  echo 'Build check failed. Deplotment aborted.'
  exit 1
fi

# Upload package to PyPi
pipenv run twine upload ${TARGET_REPO} dist/*
if [[ "${?}" -ne 0 ]]; then
  echo 'Something failed during upload.'
  exit 1
fi

# Cleanup the build directory etc.
rm -r dist build *.egg-info

echo "Upload complete!";
exit 0