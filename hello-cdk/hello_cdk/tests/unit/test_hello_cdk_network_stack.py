"""Unit tests"""

import aws_cdk as core
from aws_cdk import assertions

from hello_cdk.network_stack import NetworkStack

def test_vpc_is_created():
    """Test if a VPC is created in the NetworkStack"""

    test_config = {
        "vpc_cidr": "10.0.0.0/21"
    }
    app = core.App()
    stack = NetworkStack(app, "hello-cdk", config=test_config)
    template = assertions.Template.from_stack(stack)

    # Assert that a VPC resource is created
    template.resource_count_is("AWS::EC2::VPC", 1)
