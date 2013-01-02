all: css html

css:
	sass src/style.scss style.css

html:
	python scripts/build.py
