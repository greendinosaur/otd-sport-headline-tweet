#!/bin/sh

zipfile=function.zip
lambda_function=test-otd
data_file=data/everton_wof_new.csv

# first generate the zip file
echo Generating the zip file

# add python dependencies
zip -r9 $zipfile .venv/lib/python3.7/site-packages

# add code
zip $zipfile config.py
zip $zipfile emoji.py
zip $zipfile match.py
zip $zipfile onthisday.py
zip $zipfile tweet.py
zip $zipfile lambda_function.py

# add data files
zip $zipfile data/emoji.csv
zip $zipfile $data_file

echo Deploying to aws lambda
# now deploy
aws lambda update-function-code --function-name $lambda_function --zip-file fileb://$zipfile

# clean up
rm $zipfile