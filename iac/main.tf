/* Provider */
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.location_aws
}

/* Data */
data "aws_caller_identity" "current" {}

data "aws_ssm_parameter" "admin_unique_id" {
  name = "/core/admin_unique_id"
}

data "aws_ssm_parameter" "admin_name" {
  name = "/core/admin_name"
}

data "aws_ssm_parameter" "pipeline_runner_id" {
  name = "/core/pipeline_runner_unique_id"
}

data "aws_ssm_parameter" "pipeline_runner_name" {
  name = "/core/pipeline_runner_name"
}

data "template_file" "link_station_bucket_policy" {
  template = file("${path.module}/templates/s3-bucket-policy-link-station.json")

  vars = {
    bucket_name           = var.artifacts_s3_bucket_name
    account_id            = data.aws_caller_identity.current.account_id
    admin_id              = data.aws_ssm_parameter.admin_unique_id.value
    admin_name            = data.aws_ssm_parameter.admin_name.value
    pipeline_runner_id    = data.aws_ssm_parameter.pipeline_runner_id.value
    pipeline_runner_name  = data.aws_ssm_parameter.pipeline_runner_name.value
  }
}

/* IAM resources */
// IAM Role which grants permissions to the Lambda Function
resource "aws_iam_role" "link_station_role" {
  name                = "link-station-role"

  assume_role_policy  = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

/* S3 resources */
resource "aws_s3_bucket" "link_station_bucket" {
  bucket = var.artifacts_s3_bucket_name
}

resource "aws_s3_bucket_policy" "link_station_bucket_policy" {
  bucket = aws_s3_bucket.link_station_bucket.bucket

  policy = data.template_file.link_station_bucket_policy.rendered

  depends_on = [aws_s3_bucket.link_station_bucket]
}

resource "aws_s3_bucket_object" "artifact" {
  bucket  = var.artifacts_s3_bucket_name
  key     = var.artifacts_s3_bucket_key
  source  = "${path.module}/../target/link-station-latest.zip"

  depends_on = [aws_s3_bucket.link_station_bucket, aws_s3_bucket_policy.link_station_bucket_policy]
}

/* Lambda resources */
resource "aws_lambda_function" "link_station_lambda" {
  function_name = "link-station-function"

  s3_bucket     = aws_s3_bucket.link_station_bucket.bucket
  s3_key        = var.artifacts_s3_bucket_key

  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"

  role          = aws_iam_role.link_station_role.arn

  depends_on = [aws_s3_bucket_object.artifact]
}

/* API Gateway resources */
resource "aws_api_gateway_rest_api" "link_station_apig" {
  name        = "link-station-apig"
  description = "The API Gateway for the Link Station solution"
}

resource "aws_api_gateway_method" "Link_station_method" {
  rest_api_id   = aws_api_gateway_rest_api.link_station_apig.id
  resource_id   = aws_api_gateway_rest_api.link_station_apig.root_resource_id
  http_method   = "POST"
  authorization = "NONE"

  depends_on = [aws_api_gateway_rest_api.link_station_apig]
}

resource "aws_api_gateway_integration" "Link_station_integration" {
  rest_api_id = aws_api_gateway_rest_api.link_station_apig.id
  resource_id = aws_api_gateway_method.Link_station_method.resource_id
  http_method = aws_api_gateway_method.Link_station_method.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.link_station_lambda.invoke_arn

  depends_on = [aws_api_gateway_method.Link_station_method, aws_lambda_function.link_station_lambda]
}

resource "aws_api_gateway_deployment" "link_station_deployment" {
  rest_api_id = aws_api_gateway_rest_api.link_station_apig.id
  stage_name  = "v1"

  depends_on = [aws_api_gateway_integration.Link_station_integration]
}

resource "aws_lambda_permission" "link_station_apig" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.link_station_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.link_station_apig.execution_arn}/*/*"

  depends_on = [aws_lambda_function.link_station_lambda, aws_api_gateway_rest_api.link_station_apig]
}

output "base_url" {
  value = aws_api_gateway_deployment.link_station_deployment.invoke_url
}