#!/usr/bin/env python3

import os

import aws_cdk as cdk

from hello_cdk.db_stack import DatabaseStack
from hello_cdk.network_stack import NetworkStack

app = cdk.App()

# Usage: cdk deploy -c stack_prefix="feat-123"
stack_prefix = app.node.try_get_context("stack_prefix") or ""

# Network stack is shared amonng other branch stacks
network_stack = NetworkStack(app, "NetworkStack")
db_stack = DatabaseStack(app, stack_prefix + "DatabaseStack")

# Add dependecy so Network stack is deployet first
db_stack.add_dependency(network_stack)

# Default tags
default_tags = {
    'cost-centre':       'tbd',
    'eenvironment-type': 'nlv',
    'application':       'hello',
}

# Add default tags to all resouces
for k, v in default_tags.items():
    cdk.Tags.of(app).add(k, v)

app.synth()
