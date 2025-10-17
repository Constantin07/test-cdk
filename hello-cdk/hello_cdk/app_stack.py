"""Application stack"""

from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_logs as logs,
    aws_ec2 as ec2,
    CfnOutput,
    Fn
)

from constructs import Construct

class AppStack(Stack):                  # pylint: disable=missing-class-docstring
    def __init__(self, scope: Construct, id: str, network_stack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Set the CloudFormation template description
        self.template_options.description = "Application Stack"

        # Get the DB stack prefix from context
        db_stack_prefix = f"{self.node.try_get_context("stack_prefix") or ""}DatabaseStack"

        # Import output from another stack
        table_name = Fn.import_value(f"{db_stack_prefix}-myTableName")

        # Example SQS resource
        queue = sqs.Queue(
            self,
            id = "SQSQueue",
            queue_name = f"{id}-SQSQueue",
            retention_period = Duration.days(3),
            visibility_timeout = Duration.seconds(120),
            encryption = sqs.QueueEncryption.KMS_MANAGED,
            enforce_ssl = True
        )

        # Create a Log Group for Lambda function
        log_group = logs.LogGroup(
            self,
            id = "LogGroup",
            log_group_name = f'/aws/lambda/{id}-LogGroup' , # Physical ID
            retention = logs.RetentionDays.ONE_DAY,
            log_group_class = logs.LogGroupClass.STANDARD,
            removal_policy = RemovalPolicy.DESTROY
        )

        # Define the Lambda function resource
        my_function = _lambda.Function(
            self,
            id = "LambdaFunction",
            function_name = f"{id}-LambdaFunction",
            description = "A simple hello world Lambda function",
            runtime = _lambda.Runtime.PYTHON_3_13,
            architecture = _lambda.Architecture.ARM_64,
            handler = "lambda_function.handler",
            timeout = Duration.seconds(10),
            reserved_concurrent_executions = 10,
            log_group = log_group, # Associate the Log Group with the Lambda function
            environment = {
                "TABLE_NAME": table_name,
            },
            vpc = network_stack.vpc, # Use the VPC from NetworkStack
            vpc_subnets = ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            security_groups = [network_stack.app_security_group],
            code = _lambda.Code.from_asset("lambda.zip"),
            tracing = _lambda.Tracing.DISABLED, # cost savings
            application_log_level_v2 = _lambda.ApplicationLogLevel.INFO,
        )

        # Add dependencies
        my_function.node.add_dependency(log_group)
        my_function.node.add_dependency(queue)

        # Define the Lambda function URL resource
        my_function_url = my_function.add_function_url(
            auth_type = _lambda.FunctionUrlAuthType.NONE,
        )

        # Define a CloudFormation output(s)
        CfnOutput(self, "FunctionUrlOutput", value = my_function_url.url,
            export_name = f"{id}-FunctionUrlOutput")
        CfnOutput(self, "SqsURL", value = queue.queue_url, export_name = f"{id}-SqsURL")
