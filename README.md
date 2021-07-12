# The link station solution

## Prerequisites
- Postman, for testing purposes
- Python 3.8 or higher
- An AWS account
- A GitLab account
- A GitLab runner, or make use of the shared runners

## The solution
The solution for the defined assessment, is a Python application which consumes a JSON request.
This application is tested with unit tests and manual functional tests. It has been written to run
in AWS Lambda and is exposed via API Gateway. To deploy this solution in the AWS Cloud, I made use
of a GitLab CI/CD pipeline, which makes use of Terraform. Terraform publishes the Python application
as a .zip file in an "explicit deny" S3 Bucket, which is used by Lambda to retrieve the code. Of course,
Terraform also makes sure that the S3 Bucket is available and it creates the API Gateway for this solution.

## 1. Decisions
1. Since the team is primarily using Python, I decided to write this code in Python although
    I have more experience with Java.
2. Considering that coordinates are given for the device and link stations,
    I decided to use the Pythagoras theorem to calculate the distance as a straight line
    between the two datapoints.
3. Since the assessment statement shows that the device coordinates are specified as a tuple,
   and the link stations as a nested list, I followed the exact same data types.
4. I exposed the solution via API Gateway to make it easy to assess the solution's functionality.

## 2. Running the Python unit tests locally
Testing the application:
`python src/tests/test_lambda_function.py`

Testing the validators:
`python src/tests/test_validators.py`

## 3. Testing the solution when deployed in AWS
This can easily be done by using the API Gateway endpoint, which has the format:
https://xxxxxxxxxx.execute-api.eu-west-1.amazonaws.com/v1

In Postman, you can simply send a POST request to the API Gateway URL, and provide
the content of the event.json file as the request body.

the response would be similar to:
```
{
  "finding": "Best link station for point 0,0 is 0,0 with power 100.0"
}
```

## 4. Further improvements
To make this solution better, I would consider:
- implementing the ability to test the Lambda Function locally with the AWS SAM utility
- implementing DTAP by using AWS Organizations and GitLab CI/CD more extensively
- Implementing application versioning
- Implementing objects/classes for the device coordinates and link stations. In this way, the data types
  could be defined in a similar way, which would make it easier to compare them, or in general use them
- Implement functional testing with Newman, such that the availability of the solution in AWS is also guaranteed
- Implement security and code quality checks