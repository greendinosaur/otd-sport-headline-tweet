# Deploying to AWS Lambda
This bot can be run on as a function on AWS Lambda. You can use AWS Cloudwatch to trigger a scheduled event so that the bot runs on a periodic basis. For example, it could tweet a headline at 7am every day.

Best of all, in this scenario, it is low-usage and can run on AWS Free Tier so won't cost you a penny

# Install and Deploy

## Pre-requisites
In addition to the general pre-requisites for running the bot, in order to run this bot on AWS Lambda using the provided scripts, you will need to:
* Have set-up an AWS account
* Created a AWS user with sufficient privileges to create and edit a AWS Lambda function
* Installed the AWS CLI tool onto your local machine
* Configure the AWS CLI tool with your AWS credentials
* Added your four Twitter API credentials as Environment variables within AWS Lambda. They need to have the following keys:
    * `TWITTER_CONSUMER_KEY`
    * `TWITTER_CONSUMER_SECRET`
    * `TWITTER_ACCESS_TOKEN`
    * `TWITTER_ACCESS_TOKEN_SECRET`

## Creating the function
You can either create the function using the AWS Lambda dashboard or run a AWS CLI command to do this.

The below shows the CLI command. Prior to executing the command, make sure you have the zip file containing the code. This can be generated using the [Makefile](../Makefile). Ensure the variables at the top of the Make file are correct.

Replace `<name of function>` and `<your arn>` with your specifics.

```bash
Make package
aws lambda create-function --function-name <name of function> --zip-file fileb://function.zip --handler lambda_function.py --runtime python3.7 --role <your arn>
```

## Deploy the bot to AWS Lambda
The lambda function itself is defined in the file [lambda_function.py](../lambda_function.py). This is a simple function that calls the main code to get the headline and to tweet it.

The [Makefile](../Makefile) deploys the lambda function and associated code and python dependencies to AWS. You will need to amend two lines at the top of this file with the name of your lambda function and the data file that contains the match data.

```bash
lambda_function=test-otd
data_file=data/everton_wof_new.csv
```

The Makefile creates the deployable zip file that is deployed to AWS Lambda. This zip file contains the tweepy dependencies downloaded via pip, the necessary python files required by the main application, the data file containing match data and the lambda function. It then uploads this to AWS Lambda.

To run the script:
```bash
Make package deploy clean
```
If is successful, you will see a JSON file output containing some information about the function.

## Testing the function
You can test the lambda function via the AWS console. If you use the following JSON as the trigger event then no tweet will be generated. The code in the function handler uses the presence of the key `test` to not tweet. It ignores the value of this key.

```json
{ "test":"test"}
```

If it is successful, you will see the headline output to the terminal.

If you ran it without a key of `test` inside the triggering event then the headline will also be tweeted and appear in the bot's twitter feed.

## Setting up the AWS Cloudwatch schedule
Inside the AWS Lambda function console, you can set-up a trigger event for the function. Choose AWS Cloudwatch Events/EventWatch and enter the schedule details.

For example, enter `cron(07 06 * * ? *)` to run the bot every day at 07:06 UTC time.
