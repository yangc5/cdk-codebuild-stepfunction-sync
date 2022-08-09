import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_codebuild_stepfunction.cdk_codebuild_stepfunction_stack import CdkCodebuildStepfunctionStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_codebuild_stepfunction/cdk_codebuild_stepfunction_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkCodebuildStepfunctionStack(app, "cdk-codebuild-stepfunction")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
