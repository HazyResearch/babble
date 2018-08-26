export BABBLEHOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH="$PYTHONPATH:$BABBLEHOME"
echo "Added Babble Labble repository ($BABBLEHOME) to \$PYTHONPATH."