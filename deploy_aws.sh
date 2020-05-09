#!/bin/sh

zipfile=function.zip
lambda_function=test-otd
data_file=data/everton_wof_new.csv

cwd=$(pwd)

# install the dependencies required into a temp folder
echo installing dependencies
mkdir temp_package
pip install --target ./temp_package Tweepy

# generate the zip file
echo Generating the zip file
# firstly add the dependencies
cd package
zip -r9 $cwd/$zipfile .

echo Adding custom code
cd $cwd
# now add code
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
echo cleaning up temp files
rm $zipfile
rm -r temp_package/