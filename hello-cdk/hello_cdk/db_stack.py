from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
    aws_dynamodb as dynamodb
)

from constructs import Construct

# Define the database stack
class DatabaseStack(Stack):
    TABLE_ID = "DynamoDBTable" # Logical ID

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        config = kwargs.pop("config")
        super().__init__(scope, id, **kwargs)

        # Set the CloudFormation template description
        self.template_options.description = "Database Stack"

        # Create a new DynamoDB table
        dynamodb_table = dynamodb.Table(
            self,
            id = self.TABLE_ID,
            table_name = f"{id}-{self.TABLE_ID}",
            partition_key = dynamodb.Attribute(
                name = "id",
                type = dynamodb.AttributeType.STRING
            ),
            sort_key = dynamodb.Attribute(
                name = "timestamp",
                type = dynamodb.AttributeType.STRING
            ),
            table_class = dynamodb.TableClass.STANDARD,
            time_to_live_attribute = "expireAt",
            billing_mode = dynamodb.BillingMode.PAY_PER_REQUEST,
            # read_capacity = 5,
            # write_capacity = 5,
            encryption = dynamodb.TableEncryption.AWS_MANAGED,
            point_in_time_recovery_specification = dynamodb.PointInTimeRecoverySpecification(
                point_in_time_recovery_enabled = True
            ),
            deletion_protection = False,            # NOT recommended for production code
            removal_policy = RemovalPolicy.DESTROY  # NOT recommended for production code
        )

        dynamodb_table.add_global_secondary_index(
            index_name = "global-secondary-index",
            partition_key = dynamodb.Attribute(
                name = "gsipk",
                type = dynamodb.AttributeType.STRING
            ),
            sort_key = dynamodb.Attribute(
                name = "gsisk",
                type = dynamodb.AttributeType.STRING
            ),
            projection_type = dynamodb.ProjectionType.ALL,
        )

        # Output table ARN
        CfnOutput(self, id = "myTableName", value = dynamodb_table.table_name, export_name = f"{id}-myTableName")
