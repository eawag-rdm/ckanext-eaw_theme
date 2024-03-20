[![Tests](https://github.com/eawag-rdm/ckanext-eaw_theme/workflows/Tests/badge.svg?branch=eric)](https://github.com/eawag-rdm/ckanext-eaw_theme/actions)

# ckanext-eaw_theme

This CKAN extension provides the custom styles and templates used in EAWAG Open Data Portal. Custom validation and template snippets for editing and display are supported.
Relevant branches for **ERIC** are `eric` and the branch used for **ERIC Open** is `eric-open`. 

Files to port:

ckanext/eaw_theme/templates/footer.html
ckanext/eaw_theme/templates/group/index.html
ckanext/eaw_theme/templates/header.html
ckanext/eaw_theme/templates/home/about.html
ckanext/eaw_theme/templates/home/snippets/about_text.html
ckanext/eaw_theme/templates/organization/index.html
ckanext/eaw_theme/templates/organization/snippets/organization_item.html
ckanext/eaw_theme/templates/package/read.html
ckanext/eaw_theme/templates/package/snippets/info.html
ckanext/eaw_theme/templates/snippets/organization.html


## Requirements

**TODO:** For example, you might want to mention here which versions of CKAN this
extension works with.

If your extension works across different versions you can add the following table:

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | not tested    |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | not tested    |

Suggested values:

* "yes"
* "not tested" - I can't think of a reason why it wouldn't work
* "not yet" - there is an intention to get it working
* "no"


## Installation

**TODO:** Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-eaw_theme:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/eawag-rdm/ckanext-eaw_theme.git
    cd ckanext-eaw_theme
    pip install -e .
	pip install -r requirements.txt

3. Add `eaw_theme` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

None at present

**TODO:** Document any optional config settings here. For example:

	# The minimum number of hours to wait before re-checking a resource
	# (optional, default: 24).
	ckanext.eaw_theme.some_setting = some_default_value


## Developer installation

To install ckanext-eaw_theme for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/eawag-rdm/ckanext-eaw_theme.git
    cd ckanext-eaw_theme
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-eaw_theme

If ckanext-eaw_theme should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
