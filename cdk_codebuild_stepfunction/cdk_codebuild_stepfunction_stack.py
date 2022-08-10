import aws_cdk as cdk
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda,
    aws_iam,
    aws_s3,
    aws_s3_deployment as s3deploy,
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

# S3 bucket for CodeBuild artifacts including buildspec.yml
        codebuild_artifacts_bucket = aws_s3.Bucket(self, "codebuild-bucket", bucket_name="cdk-codebuild-stepfunction-demo-artifacts-bucket",versioned=True)

# S3 deployment to upload buildspec.yml for city codebuild project and use it as codebuild source for city Project
        city_codebuild_bucket_deployment = s3deploy.BucketDeployment(self, "city-codebuild-artifacts-bucket-deployment",
            sources=[s3deploy.Source.asset("city_codebuild")],
            destination_bucket=codebuild_artifacts_bucket,
            destination_key_prefix="city"
        )

        city_codebuild_s3_source = codebuild.Source.s3(
            bucket=codebuild_artifacts_bucket,
            path="city/"
        )

        city_codebuild_project = codebuild.Project(self, "city-codebuild-project",
            project_name="city-codebuild-project",
            source=city_codebuild_s3_source,
            environment_variables={
                "CITY": codebuild.BuildEnvironmentVariable(
                    value="placeholder"
                )
            }
        )

        codebuild_artifacts_bucket.grant_read(city_codebuild_project.role)
