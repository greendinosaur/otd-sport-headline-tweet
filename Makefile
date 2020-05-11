# The binary to build (just the basename).
MODULE := blueprint

AWS_ZIPFILE :=function.zip
LAMBDA_FUNCTION :=test-otd
data_file :=data/everton_wof_new.csv
AWS_DEPLOY_OUTPUT := aws_deploy_output.json

cwd:= $(shell pwd)

MODULE := main.py

BLUE='\033[0;34m'
NC='\033[0m' # No Color

# This version-strategy uses git tags to set the version string
TAG := $(shell git describe --tags --always --dirty)

run:
	@python -m $(MODULE)

test:
# pytest is not generating coverage data files for some reason
# using coverage directly
#	@pytest
	@coverage run -m pytest 
	@coverage xml

lint:
	@echo "\n${BLUE}Running Pylint against source and test files...${NC}\n"
	@pylint --rcfile=setup.cfg **/*.py
	@echo "\n${BLUE}Running Flake8 against source and test files...${NC}\n"
	@flake8
	@echo "\n${BLUE}Running Bandit against source files...${NC}\n"
	@bandit -r --ini setup.cfg

sonar:
	@sonar-scanner

version:
	@echo $(TAG)

.PHONY: clean test

clean:
	@rm -rf .pytest_cache __pycache__ tests/__pycache__ .coverage tests/.pytest_cache coverage.xml
	@rm -rf temp_package
	@rm $(AWS_ZIPFILE)
	@rm $(AWS_DEPLOY_OUTPUT)

package:
	@echo $(cwd)

	# install the dependencies required into a temp folder
	@echo installing dependencies
	@mkdir temp_package
	@pip install --target ./temp_package Tweepy

	# generate the zip file
	@echo Generating the zip file
	# firstly add the dependencies
	@cd temp_package && zip -r9 $(cwd)/$(AWS_ZIPFILE) .
	@echo Adding custom code
	# now add code
	@zip $(AWS_ZIPFILE) config.py
	@zip $(AWS_ZIPFILE) emoji.py
	@zip $(AWS_ZIPFILE) match.py
	@zip $(AWS_ZIPFILE) onthisday.py
	@zip $(AWS_ZIPFILE) tweet.py
	@zip $(AWS_ZIPFILE) lambda_function.py

	# add data files
	@zip $(AWS_ZIPFILE) data/emoji.csv
	@zip $(AWS_ZIPFILE) $(data_file)

deploy:
	@aws lambda update-function-code --function-name $(LAMBDA_FUNCTION) --zip-file fileb://$(AWS_ZIPFILE) >> $(AWS_DEPLOY_OUTPUT)

