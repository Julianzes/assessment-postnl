# 4 - Developer Associate

The development team at a retail organization wants to allow a Lambda function in its AWS Account A to access a DynamoDB table in another AWS Account B.

<p align="center">
<img src="../assets/diagrams/Picture 4.png?raw=true" style="background-color:white" width="75%">
</p>

<br>

```
As a Developer, which solution(s) would you recommend?
```

Answer:
In this case i would create a role in AWS Account B that is assumable by the Lambda from AWS Account A. This role can then have only the neccesary authorisations the Lambda needs to access the Dynamodb Table.

