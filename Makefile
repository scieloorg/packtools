clean:
	@python setup.py clean
	@rm -f dist/*

build:
	@python setup.py sdist
	@cd dist; ls *.tar.gz | xargs python -m pip wheel --no-deps -w .

upload:
	@twine upload dist/*


.PHONY: clean build upload
