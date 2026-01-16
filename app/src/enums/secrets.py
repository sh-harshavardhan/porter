from enum import Enum


class SecretSource(Enum):
    aws_sm = 'aws_sm'
    aws_ssm = 'aws_ssm'
    gcp_sm = 'gcp_sm'
    azure_kv = 'azure_kv'
    hashicorp_vault = 'hashicorp_vault'
