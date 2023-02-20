test:
	python -m pytest --ckan-ini=test.ini

setup-dev: requirements_dev.txt
	pip install -r requirements_dev.txt

reformat:
	isort ckanext/
	black ckanext/
	djlint ckanext/eaw_theme/templates/ --reformat
	djlint _templates_v2.7.3 --reformat


