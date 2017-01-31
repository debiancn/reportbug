#! /usr/bin/make -f

NOSETESTS = nosetests3 test -v --stop
nosetests_cmd = $(NOSETESTS) ${NOSETESTS_OPTS}

.PHONY: tests
tests:
	$(nosetests_cmd)

# run tests not requiring network
.PHONY: quicktests
quicktests: NOSETESTS_OPTS += --processes=4 --attr='!network'
quicktests:
	$(nosetests_cmd)

coverage: NOSETESTS_OPTS += --with-coverage --cover-package=reportbug
coverage:
	$(nosetests_cmd)

coverhtml: NOSETESTS_OPTS += --cover-html
coverhtml: coverage

codechecks: pep8 pyflakes pylint

pep8:
	pep8 --verbose --repeat --show-source --filename=*.py,reportbug,querybts . --statistics --ignore=E501

pyflakes:
	pyflakes . bin/*

pylint:
	pylint --output-format=colorized  bin/* reportbug/ checks/* test/ setup.py

.PHONY: i18n
i18n:
	xgettext \
	    --language=Python \
	    --default-domain=reportbug \
	    --output-dir=po \
		-o reportbug.pot \
		bin/reportbug
	xgettext \
	    --language=Python \
	    --default-domain=python3-reportbug \
	    --output-dir=po \
	    -o python3-reportbug.pot \
		reportbug/*.py \
		reportbug/ui/*.py
	(for i in po/*/reportbug.*.po; do msgmerge -U $${i} po/reportbug.pot; done)
	(for i in po/*/python3-reportbug.*.po; do msgmerge -U $${i} po/python3-reportbug.pot; done)

.PHONY: generate-translations
generate-translations:
	(for i in po/*/reportbug.*.po; do \
	    _f="$$(dirname $${i})/reportbug.mo"; \
	    msgfmt $${i} -o $$_f; \
	 done)
	(for i in po/*/python3-reportbug.*.po; do \
	    _f="$$(dirname $${i})/python3-reportbug.mo"; \
	    msgfmt $${i} -o $$_f; \
	 done)
