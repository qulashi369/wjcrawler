echo 'init virtuallenv'
virtualenv --no-site-packages .
source bin/activate

echo 'install dependents'
bin/pip install -r requirements.txt
