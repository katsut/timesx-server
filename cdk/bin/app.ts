#!/usr/bin/env node

import { PythonFunction, PythonLayerVersion } from '@aws-cdk/aws-lambda-python-alpha'
import * as cdk from 'aws-cdk-lib'
import { LambdaIntegration, RestApi } from 'aws-cdk-lib/aws-apigateway'
import { Runtime } from 'aws-cdk-lib/aws-lambda'
import { Construct } from 'constructs'

class TimesXStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props)
    const startingTime = new Date()

    console.log(`#################`)
    console.log(`Start Archive at ${startingTime.toLocaleTimeString()}`)
    console.log(`################`)


    // Create a Python Lambda function
    const lambdaFunction = new PythonFunction(this, 'receiveRawText', {
      runtime: Runtime.PYTHON_3_11,
      handler: 'handler',
      index: 'handler.py',
      entry: '../',
      timeout: cdk.Duration.seconds(300),
      memorySize: 128,
      bundling: {
        // translates to `rsync --exclude='.venv'`
        assetExcludes: ['.venv', '.vscode', '*.code-workspace', 'cdk', '.git']
      }
    })

    // Create an API Gateway REST API
    const api = new RestApi(this, 'TimesXApi')

    // Create an API Gateway resource and associate the Lambda function
    const lambdaIntegration = new LambdaIntegration(lambdaFunction)
    api.root.addResource('api').addMethod('POST', lambdaIntegration)
  }
}

const app = new cdk.App()
new TimesXStack(app, 'TimesXStack')
app.synth()
