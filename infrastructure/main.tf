terraform {
  backend "s3" {
    bucket  = "dallas-pets-alive-terraform"
    key     = "new_digs.tfstate"
    region  = "us-east-2"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.11.0"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-east-2"
}

resource "aws_db_instance" "new_digs" {
  allocated_storage             = 10
  db_name                       = "new_digs"
  engine                        = "postgres"
  engine_version                = "14"
  identifier                    = "new-digs"
  instance_class                = "db.t3.micro"
  manage_master_user_password   = true
  username                      = "dallaspetsalive"
  backup_retention_period       = 7
  apply_immediately             = true
}
