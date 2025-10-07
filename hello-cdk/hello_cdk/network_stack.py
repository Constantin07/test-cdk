"""Network stack"""

from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_ec2 as ec2
)

from constructs import Construct

class NetworkStack(Stack):              # pylint: disable=missing-class-docstring
    VPC_ID = "Vpc" # Logical ID

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        config = kwargs.pop("config")
        super().__init__(scope, id, **kwargs)

        # Set the CloudFormation template description
        self.template_options.description = "Networking Stack (Shared)"

        vpc_cidr = config["vpc_cidr"]

        # Create VPC
        vpc = ec2.Vpc(
            self,
            id = self.VPC_ID,
            vpc_name = f"{id}-{self.VPC_ID}",
            max_azs = 2,
            ip_addresses = ec2.IpAddresses.cidr(vpc_cidr),
            ip_protocol = ec2.IpProtocol.IPV4_ONLY,
            default_instance_tenancy = ec2.DefaultInstanceTenancy.DEFAULT,
            create_internet_gateway = True,
            enable_dns_hostnames = True,
            enable_dns_support = True,
            nat_gateway_provider = ec2.NatGatewayProvider.gateway(),
            nat_gateways = 0,
            restrict_default_security_group = False,
            vpn_gateway = False,
            subnet_configuration = [
                # Public Subnets
                ec2.SubnetConfiguration(
                    name = "public",
                    subnet_type = ec2.SubnetType.PUBLIC,
                    cidr_mask = 24,
                    map_public_ip_on_launch = True,
                ),
                # Private Subnets (App)
                ec2.SubnetConfiguration(
                    name = "private-app",
                    subnet_type = ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask = 24,
                ),
                # Private Subnets (DB)
                ec2.SubnetConfiguration(
                    name = "private-db",
                    subnet_type = ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask = 24,
                ),
            ],
            gateway_endpoints = {
                "S3": ec2.GatewayVpcEndpointOptions(
                    service = ec2.GatewayVpcEndpointAwsService.S3
                ),
                "DynamoDb": ec2.GatewayVpcEndpointOptions(
                    service = ec2.GatewayVpcEndpointAwsService.DYNAMODB
                )
            }
        )

        vpc.apply_removal_policy(RemovalPolicy.DESTROY)
