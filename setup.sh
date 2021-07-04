# Usage documentation
usage() { echo "Usage: $0 [-d] [-f]" 1>&2; exit 1; }

help () {
    echo "Options :"
    echo "    -f Force        Forces the recreation of the requirements files"
    echo "    -d Development  Builds the development requirements and install them as well"
    exit
}

while getopts "dfh" option; do
    case ${option} in
        f )
        FORCE="true"
        ;;
        d )
        DEV="true"
        ;;
        h )
        help
        ;;
        \? ) #For invalid option
        usage
        ;;
    esac
done

# Try venv installation
{
    python3 -m venv ve
} || {
    echo "Unable to create a virtual environment, make sure python3-virtualenv is installed !"
}

source ve/bin/activate

# Build requirements if needed
if [ ! -e requirements/requirements.txt ] || ([ ! -e requirements/requirements-dev.txt ] && [ "$DEV" == "true" ]) || [ "$FORCE" == "true" ]; then
    pip install pip-tools

    if [ "$DEV" == "true" ]; then
        ./requirements/build_requirements.sh dev
    else
        ./requirements/build_requirements.sh
    fi
fi

# Install requirements
pip install -r requirements/requirements.txt
if [ "$DEV" == "true" ]; then
    pip install -r requirements/requirements-dev.txt
fi

./manage.py migrate
