#!/usr/bin/env python3

import os

import aws_cdk as cdk

from hello_cdk.config import load_config
from hello_cdk.network_stack import NetworkStack
from hello_cdk.db_stack import DatabaseStack
from hello_cdk.app_stack import AppStack

app = cdk.App()

# Usage: cdk deploy -c stack_prefix="feat-123-branch-name-"
stack_prefix = app.node.try_get_context("stack_prefix") or ""

# Load environment configuration from YAML file
env_name = app.node.try_get_context("env") or "dev" # Default to 'dev' if not provided
if not env_name:
    raise RuntimeError("The mandatory environment context 'env' is not set. Use -c env=dev")
else:
    print(f"Environment: {env_name}")
config = load_config(env_name)

# Network stack is shared with other branch stacks
network_stack = NetworkStack(app, "NetworkStack", config=config)
db_stack = DatabaseStack(app, stack_prefix + "DatabaseStack", config=config)
app_stack = AppStack(app, stack_prefix + "AppStack", config=config)

# Add dependecy so Network stack is deployet first
db_stack.add_dependency(network_stack)
app_stack.add_dependency(network_stack)
app_stack.add_dependency(db_stack)

# Add default tags to all resouces
for k, v in config["default_tags"].items():
    cdk.Tags.of(app).add(k, v)

app.synth()
