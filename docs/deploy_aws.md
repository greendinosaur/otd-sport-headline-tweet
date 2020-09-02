# Deploying to AWS Lambda

This bot can be run on as a function on AWS Lambda. You can use AWS Cloudwatch to trigger a scheduled event so that the bot runs on a periodic basis. For example, it could tweet a headline at 7am every day.

Best of all, in this scenario, it is low-usage and can run on AWS Free Tier so won't cost you a penny

## Install and Deploy

### Pre-requisites

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
  * The keys are to be encrypted using the Lambda environment variable encryption options. Check out this [document](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html) for further information. If you don't wish to encrypt the keys then amend the default lambda handler `lambda_function.py`

You can now either use (i) a combination of the AWS CLI and AWS dashboard to deploy the application or (ii) use AWS SAM. Both options are described below.

## Install and Deploy via AWS CLI and AWS Dashboard

The following instructions can help you set-up the function using the AWS CLI and the AWS Dashboard

### Creating the function

You can either create the function using the AWS Lambda dashboard or run a AWS CLI command to do this.

The below shows the CLI command. Prior to executing the command, make sure you have the zip file containing the code. This can be generated using the [Makefile](../Makefile). Ensure the variables at the top of the Make file are correct.

Replace `<name of function>` and `<your arn>` with your specifics.

`lambda_function.py` is the handler that is invoked by an event. It expects the environment variables to be encrypted using a key stored in AWS KMS and to which your lambda role has access to: it uses the boto3 library to decrypt the environment variables.

```bash
Make package
aws lambda create-function --function-name <name of function> --zip-file fileb://function.zip --handler lambda_function.py --runtime python3.7 --role <your arn>
```

### Deploy the bot to AWS Lambda

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

### Testing the function

You can test the lambda function via the AWS console. If you use the following JSON as the trigger event then no tweet will be generated. The code in the function handler uses the presence of the key `test` to not tweet. It ignores the value of this key.

```json
{ "test":"test"}
```

If it is successful, you will see the headline output to the terminal.

If you ran it without a key of `test` inside the triggering event then the headline will also be tweeted and appear in the bot's twitter feed.

### Setting up the AWS Cloudwatch schedule

Inside the AWS Lambda function console, you can set-up a trigger event for the function. Choose AWS Cloudwatch Events/EventWatch and enter the schedule details.

For example, enter `cron(07 06 * * ? *)` to run the bot every day at 07:06 UTC time.

## Deploy via AWS SAM

The file [template.yaml](../template.yaml) is a AWS SAM template that enables the lambda function to be created within a dedicated Cloud Formation Stack. It also creates a scheduler to automatically execute the lambda function.

### Pre-requisites for using AWS SAM

* Ensure the AWS SAM tool is installed onto your local machine.
* Create a S3 bucket to store the uploaded code. This can be created via `aws s3 mb s3://BUCKET_NAME`. Make a note of this bucket.
* Install Docker desktop (see below for rationale)
* As above, there is some initial configuration to be made via the AWS dashboard. This is a one-off:
  * ensure there is a role within AWS IAM that can execute lambda functions. Make a note of this. You will need it's ARN value: this will begin with `arn:aws:iam::`
  * create a key within KMS to be used to encrypt the environment variables, ensure the IAM role has access to use this key. Make a note of the ARN of the key: it will begin with `arn:aws:kms:`
  * encrypt the four twitter related environment variables using this key and have the encrypted values available

### Build and deploy via AWS SAM

To build, package and deploy the function, execute each of the lines in turn in the base directory of the application.:

```bash
sam build --use-container
sam package --s3-bucket <YOUR_BUCKET_NAME> --output-template-file output.yaml
sam deploy --template-file output.yaml --stack-name <YOUR_STACK_NAME> --capabilities CAPABILITY_IAM --parameter-overrides CONSUMERKEY=<YOUR_TWITTER_CONSUMER_KEY> CONSUMERSECRET=<YOUR_TWITTER_CONSUMER_SECRET> ACCESSTOKEN=<YOUR_TWITTER_ACCESS_KEY> ACCESSTOKENSECRET=<YOUR_TWITTER_ACCESS_SECRET> LAMBDAROLE=<YOUR_LAMBDA_ROLE> KMSKEY=<YOUR_KMS_KEY>
```

To view details about the newly created stack and function, enter

```bash
aws cloudformation describe-stacks --stack-name <YOUR_STACK_NAME>
```

This will output details about the stack as well as the function name. Make a note of the function ARN in order to test it.

To execute the function from the command-line

```bash
aws lambda invoke  --cli-binary-format raw-in-base64-out --function-name <ARN_OF_THE_FUNCTION> --payload '{ "test": "test" }' response.json
```

This should give a status code of 200 and the generated `response.json` file should contain a headline generated for this day in history. The `payload` parameter stops it from tweeting. If you want to test the tweet functionality then execute the above without the `payload` parameter as:

```bash
aws lambda invoke  --cli-binary-format raw-in-base64-out --function-name <ARN_OF_THE_FUNCTION> response.json
```

#### Why is Docker Desktop required

The `sam build --use-container` command detailed above requires Docker Desktop to be installed. This is because some of the python library dependencies are not available as wheels. If the simpler `sam build` command is used then it fails due to the lack of wheels. An alternative is to use lambda layers and specify these within the SAM template but I have not explored this option.

This article on [Real Python](https://realpython.com/python-wheels/) explains wheels if you're not familiar with them.
