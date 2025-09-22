#!/usr/bin/env python3

import os

import aws_cdk as cdk

from hello_cdk.db_stack import DatabaseStack

app = cdk.App()

# Usage: cdk deploy -c stack_prefix="feat/123"
stack_prefix = app.node.try_get_context("stack_prefix") or ""

db_stack = DatabaseStack(app, stack_prefix + "DatabaseStack")

app.synth()
