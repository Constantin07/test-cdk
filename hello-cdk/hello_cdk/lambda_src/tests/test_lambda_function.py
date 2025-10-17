"""Unit tests for Test Lambda function"""

import os
import json
from unittest import TestCase
from unittest.mock import patch

# Import from Lambda handler
from hello_cdk.lambda_src.lambda_function import handler

class TestLambda(TestCase):
    """Test class for AWS Lambda Function"""

    def test_handler_with_env_vars_set(self):
        """Test with env var set"""

        with patch.dict(os.environ, {"TABLE_NAME": "TestTable"}, clear=False):
            resp = handler({}, None)
            self.assertEqual(resp["statusCode"], 200)
            self.assertEqual(json.loads(resp["body"]),
                "Hello CDK App! Table name is: TestTable")
