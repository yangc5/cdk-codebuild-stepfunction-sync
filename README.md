
# Deploy a Step Function with Synchronous CodeBuild Steps Using CDK (Python)

This artifact will help you create a Step Function composed of a couple CodeBuild steps using CDK (Python). What’s worth noting is by default Step Functions deployed by CDK (Python) orchestrate CodeBuild tasks asynchronously, i.e., it does not wait for one CodeBuild task to finish successfully before starting the next step. This behavior can be problematic when a subsequent step depends on a CodeBuild task’s output.

The workaround is to use a Lambda Function as a wrapper to start a CodeBuild project and poll the status. By default Step Functions wait for Lambda Function tasks to execute successfully before starting the next step. This set up solves the asynchronous problem of orchestrating CodeBuild tasks using Step Functions.

## Prerequisites 

[AWS CLI](https://cdkworkshop.com/15-prerequisites/100-awscli.html)

[AWS Account and User](https://cdkworkshop.com/15-prerequisites/200-account.html)

[Node.js](https://cdkworkshop.com/15-prerequisites/300-nodejs.html)

[IDE for your programming language](https://cdkworkshop.com/15-prerequisites/400-ide.html)

[AWS CDK Toolkit](https://cdkworkshop.com/15-prerequisites/500-toolkit.html)

[Python](https://cdkworkshop.com/15-prerequisites/600-python.html)

## CDK deploy

To make an initial cdk deployment to deploy the solution. Bootstrap to your desired aws account and region and then deploy:
```
    cdk bootstrap aws://[ACCOUNT_ID]/[REGION]
    cdk synth
    cdk deploy
```
