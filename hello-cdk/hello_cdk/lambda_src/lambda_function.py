"""
Test Lambda function
"""

import os
import json

def handler(event, context):        # pylint: disable=unused-argument
    """AWS Lambda entry point."""

    table_name = (os.environ.get("TABLE_NAME") or "None").strip()
    return {
        "statusCode": 200,
        "body": json.dumps(f"Hello CDK App! Table name is: {table_name}")
    }
