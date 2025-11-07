"""Application stack"""

from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_logs as logs,
    aws_ec2 as ec2,
    aws_iam as iam,
    BundlingOptions,
    CfnOutput,
    Fn
)

from constructs import Construct

class AppStack(Stack):                  # pylint: disable=missing-class-docstring
    def __init__(self, scope: Construct, id: str, config, network_stack, **kwargs) -> None:
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

        # Lambda code
        code = _lambda.Code.from_asset(
            path = "hello_cdk/lambda_src",
            bundling = BundlingOptions(
                image = _lambda.Runtime.PYTHON_3_13.bundling_image, # pylint: disable=no-member
                command = [
                    "bash", "-c",
                    # install deps
                    "pip3 install -r requirements.txt -t /asset-output && " +
                    "cp -a . /asset-output && " +
                    # prune unwanted files from the bundle
                    "rm -rf /asset-output/tests && " +
                    "find /asset-output -type d -name '__pycache__' -prune -exec rm -rf {} + && " +
                    "find /asset-output -type f -name '*.pyc' -delete"
                ],
            ),
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
            timeout = Duration.seconds(30),
            reserved_concurrent_executions = 10,
            log_group = log_group, # Associate the Log Group with the Lambda function
            environment = {
                "TABLE_NAME": table_name,
            },
            vpc = network_stack.vpc, # Use the VPC from NetworkStack
            vpc_subnets = ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            security_groups = [network_stack.app_security_group],
            code = code,
            tracing = _lambda.Tracing.DISABLED, # cost savings
            application_log_level_v2 = _lambda.ApplicationLogLevel.INFO,
            logging_format = _lambda.LoggingFormat.JSON
        )

        # Create new published version
        version = my_function.current_version

        # Create an alias that points to the latest version
        alias = _lambda.Alias(
            self,
            "MyLambdaAlias",
            alias_name = config["environment"],
            version=version
        )

        # Add permissions to the alias
        alias.add_permission(
            "InvokeFromApiGw",
            principal = iam.ServicePrincipal("apigateway.amazonaws.com"),
            action = "lambda:InvokeFunction",
            source_account = Stack.of(self).account,
        )

        # Define the Lambda function URL resource
        my_function_url = my_function.add_function_url(
            auth_type = _lambda.FunctionUrlAuthType.NONE,
        )

        # Add dependencies
        my_function.node.add_dependency(log_group)
        my_function.node.add_dependency(queue)

        # Define a CloudFormation output(s)
        CfnOutput(self, "FunctionUrl", value = my_function_url.url,
            export_name = f"{id}-FunctionUrl")
        CfnOutput(self, "SqsURL", value = queue.queue_url, export_name = f"{id}-SqsURL")
