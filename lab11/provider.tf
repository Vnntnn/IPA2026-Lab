provider "aws" {
  region     = "us-east-1"
  access_key = ""
  secret_key = ""
  token      = ""
  default_tags {
    tags = {
      Course    = "IPA-Terraform"
      ManagedBy = "Terraform"
    }
  }
}