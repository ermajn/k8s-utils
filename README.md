# K8s-utils

Set of utility scripts written to modify ceratin Kubernetes resources massivly

## Pyton virtual evnironment

* Install the venv of the specific Python version
  $ sudo apt install python<version>-venv  
  (Ex: sudo apt install python3.10-venv)  

* create venv
  $ python<version> -m venv <virtual-environment-name>  
  (Ex: python3.10 -m venv venv_3_10)

* activate the Virtual Environment  
  $ source venv_3_10/bin/activate

* install pipenv in Virtual Environment
  $ pip3 install pipenv --upgrade

* install all dependencies in the pipfile
  $ pipenv install

* deactivate a Virtual Environment  
  $ deactivate
