upload_to_pip:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*


.PHONY: test