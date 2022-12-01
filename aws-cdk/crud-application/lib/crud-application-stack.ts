import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { aws_apigateway, aws_lambda, aws_iam, aws_dynamodb } from 'aws-cdk-lib';
import { join } from 'path';
import { ManagedPolicy, PolicyStatement } from 'aws-cdk-lib/aws-iam';


export class CrudApplicationStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);


    const booksTable = new aws_dynamodb.Table(this, 'Table', {
      tableName: "books-table",
      partitionKey: { name: 'isbn', type: aws_dynamodb.AttributeType.STRING },
      billingMode: aws_dynamodb.BillingMode.PROVISIONED,
      encryption: aws_dynamodb.TableEncryption.AWS_MANAGED,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const myLambdaRole = new aws_iam.Role(this, 'myLambdaRole', {
      roleName: "crud-lambdas-role",
      assumedBy: new aws_iam.ServicePrincipal('lambda.amazonaws.com'),
    });

    myLambdaRole.addToPolicy(new PolicyStatement({
      resources: [booksTable.tableArn],
      actions: [
        'dynamodb:PutItem',
        'dynamodb:DeleteItem',
        'dynamodb:GetItem',
        'dynamodb:Scan',
        'dynamodb:UpdateItem'
      ],
    }));
    myLambdaRole.addToPolicy(new PolicyStatement({
      resources: ["*"],
      actions: [
        'logs:CreateLogGroup',
        'logs:CreateLogStream',
        'logs:PutLogEvents'
      ],
    }));

    const createRecordLambda = new aws_lambda.Function(this, 'createRecordLambda', {
      functionName: "create-record",
      runtime: aws_lambda.Runtime.PYTHON_3_8,
      handler: 'create_record.lambda_handler',
      code: aws_lambda.Code.fromAsset(join(__dirname, '../src')),
      role: myLambdaRole,
      environment: {
        'TABLE_NAME': booksTable.tableName,
      }
    });

    const deleteRecordLambda = new aws_lambda.Function(this, 'deleteRecordLambda', {
      functionName: "delete-record",
      runtime: aws_lambda.Runtime.PYTHON_3_8,
      handler: 'delete_record.lambda_handler',
      code: aws_lambda.Code.fromAsset(join(__dirname, '../src')),
      role: myLambdaRole,
      environment: {
        'TABLE_NAME': booksTable.tableName,
      }
    });

    const updateRecordLambda = new aws_lambda.Function(this, 'updateRecordLambda', {
      functionName: "update-record",
      runtime: aws_lambda.Runtime.PYTHON_3_8,
      handler: 'update_record.lambda_handler',
      code: aws_lambda.Code.fromAsset(join(__dirname, '../src')),
      role: myLambdaRole,
      environment: {
        'TABLE_NAME': booksTable.tableName,
      }
    });

    const queryRecordLambda = new aws_lambda.Function(this, 'queryRecordLambda', {
      functionName: "query-record",
      runtime: aws_lambda.Runtime.PYTHON_3_8,
      handler: 'query_record.lambda_handler',
      code: aws_lambda.Code.fromAsset(join(__dirname, '../src')),
      role: myLambdaRole,
      environment: {
        'TABLE_NAME': booksTable.tableName,
      }
    });    

    const api = new aws_apigateway.RestApi(this, 'booksApi');


    const books = api.root.addResource('books');
    books.addMethod('POST', new aws_apigateway.LambdaIntegration(createRecordLambda));
    books.addMethod('PUT', new aws_apigateway.LambdaIntegration(updateRecordLambda));

    const isbn = books.addResource('{isbn}');
    isbn.addMethod('GET', new aws_apigateway.LambdaIntegration(queryRecordLambda));
    isbn.addMethod('DELETE', new aws_apigateway.LambdaIntegration(deleteRecordLambda));
  }
}
