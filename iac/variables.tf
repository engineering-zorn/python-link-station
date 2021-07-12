/* Provider */
variable "location_aws" {
  description = "The AWS Region in which the resources are deployed"
}

/* S3 variables */
variable "artifacts_s3_bucket_name" {
  description = "The S3 Bucket location containing the application artifacts"
}

variable "artifacts_s3_bucket_key" {
  description = "The S3 Object Key of the application's artifact"
}