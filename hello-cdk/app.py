#!/usr/bin/env python3

import os

import aws_cdk as cdk

from hello_cdk.db_stack import DatabaseStack

app = cdk.App()

db_stack = DatabaseStack(app, "DatabaseStack")

app.synth()
