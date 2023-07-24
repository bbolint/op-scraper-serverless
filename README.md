# Lean Oddsportal scraper deployable on the AWS cloud using Lambda and Docker.

The scraper scrapes pages of Oddsportal where aggregated (AVG) odds are shown for each game event, by feeding the AWS Lambda function with the following trigger information:
{
  "oddsportal link":"save destination on AWS S3"
  e.g.: "https://www.oddsportal.com/hockey/usa/nhl-2022-2023/results/#/page/1":"s3://bucket-name/folder-name/folder-name/1X2-AVG/"
}

The function saves the odds data from https://www.oddsportal.com/hockey/usa/nhl-2022-2023/results/#/page/1 into a structured parquet file on s3 containing all relevant information from the website in a table format.

## Deployment instructions

1. Install serverless and docker.
2. You may create your own serverless and AWS config using the terminal or the json files.
3. Serverless deploy command compiles the docker image containing the scraper, pushes it to AWS ECS and deploys the respective Lambda function.
4. The deployed Lambda function can be invoked using a python API based on the frame "send_jobs_lambda.py".
