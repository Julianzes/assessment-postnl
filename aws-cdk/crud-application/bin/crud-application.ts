#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { CrudApplicationStack } from '../lib/crud-application-stack';

const app = new cdk.App();
new CrudApplicationStack(app, 'CrudApplicationStack', {
  env: { account: '063717074857', region: 'eu-west-1' },
});