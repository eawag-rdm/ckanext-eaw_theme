=============
ckanext-eaw_theme
=============

* provides Eawag logo
* provides Eawag favicon
* provides spatial search display
 
------------
Requirements
------------

tested for CKAN v2.4.1

------------
Installation
------------

To install ckanext-eaw_theme:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-eaw_theme Python package into your virtual environment::

     pip install ckanext-eaw_theme

3. Add ``eaw_theme`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload

------------------------
Development Installation
------------------------

To install ckanext-eaw_theme for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/eawag-rdm/ckanext-eaw_theme.git
    cd ckanext-eaw_theme
    python setup.py develop
    pip install -r dev-requirements.txt
