=============
ckanext-open_alberta
=============

Ckan theme for open.alberta.ca

------------
Requirements
------------

Ckan 2.3.x release/
CentOS/Rhel 7.x
Postgresql9.x

------------
Installation
------------

To install ckanext-open_alberta:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-open_alberta Python package into your virtual environment::

3. Add ``open_alberta`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/development.ini``).

4. Restart CKAN.::

     sudo systemctl restart httpd


---------------
Config Settings
---------------

    ckan.plugins = ... open_alberta openalbertapages

License edit license.json:

    set the licenses_group_url
    licenses_group_url = file:///usr/lib/ckan/default/src/ckanext-open_alberta/ckanext/open_alberta/public/licenses.json

    update package set license_id = 'Alberta Queens Printer Terms of Use' where license_id = 'QPTU';
    update package set license_id = 'Open Government Licence -Alberta' where license_id = 'OGLA';
    update package set license_id = 'Open Government Licence -Alberta' where license_id = 'ABOGPL';

    

------------------------
Development Installation
------------------------

To install ckanext-open_alberta for development, activate your CKAN virtualenv and do::

    git clone --recursive https://github.com/abgov/ckanext-open_alberta.git
    Get the stable branch only
    git clone --recursive https://github.com/abgov/ckanext-open_alberta.git --branch stable

    cd ckanext-open_alberta
    python setup.py develop

    pip install -r dev-requirements.txt


------------
CKAN Theming
------------

Links::

    http://docs.ckan.org/en/latest/theming/
    http://ckan.readthedocs.org/en/ckan-2.2/theming.html

Jinja::

    http://jinja.pocoo.org/
    http://jinja.pocoo.org/docs/dev/

Ckan theme files reside mostly under::

    ckanext-open_alberta/ckanext/open_alberta/ 

Default ckan 2.2 templates are under::

    ckanext-open_alberta/ckan_default_templates/ 

To update your submodules in your repo::

    git submodule update --init --recursive



-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.open_alberta --cover-inclusive --cover-erase --cover-tests
