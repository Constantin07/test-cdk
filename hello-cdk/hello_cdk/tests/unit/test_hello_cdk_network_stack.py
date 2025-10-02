import aws_cdk as core
import aws_cdk.assertions as assertions

from hello_cdk.network_stack import NetworkStack

def test_vpc_is_created():

    app = core.App()
    stack = NetworkStack(app, "hello-cdk", config={})
    template = assertions.Template.from_stack(stack)

    # Assert that a VPC resource is created
    template.resource_count_is("AWS::EC2::VPC", 1)
