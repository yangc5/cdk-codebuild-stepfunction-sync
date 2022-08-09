import aws_cdk as cdk
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda,
    aws_iam,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_codebuild as codebuild
)
from constructs import Construct

class CdkCodebuildStepfunctionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

# Grant Lambda permissions for StartBuild and BatchGet* actions for codebuild resources
        codebuild_statement=aws_iam.PolicyStatement(
            actions=["codebuild:StartBuild","codebuild:BatchGet*"],
            resources=["*"]
        )

# Helper lambda to call CodeBuild projects in Step Functions
        codebuild_lambda = aws_lambda.Function(
            self, "codebuild-function",
            function_name="codebuild-function",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="codebuild_lambda.handler",
            code=aws_lambda.Code.from_asset("./lambdas"),
            timeout=cdk.Duration.minutes(10)
        )

# Attach CodeBuild policy to Lambda execution role
        codebuild_lambda.role.add_to_policy(codebuild_statement)
