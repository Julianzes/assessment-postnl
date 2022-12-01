# Welcome to my CRUD Application - CDK TypeScript project

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template


## API Instructions

Below you will find instructions on how to use the APi. Examples are given.

### Create record
To create a record use PUT with the following body:
POST /books
```json
{
    "payload": [
        {
            "name": "<string>",
            "isbn": "<string>",
            "authors": "<string>",
            "languages": "<string>",
            "countries": "<string>",
            "numberOfPages": "<string>",
            "releaseDate": "<string>"
        },
        {
            "name": "<string>",
            "isbn": "<string>",
            "authors": "<string>",
            "languages": "<string>",
            "countries": "<string>",
            "numberOfPages": "<string>",
            "releaseDate": "<string>"
        }
    ]
}
```
One or multiple books can be added at the same time.

### Update record
To update a record use PUT with the following body.
PUT /books
``` json
{
    "payload": {
        {
            "name": "<string>",
            "isbn": "<string>",
            "authors": "<string>",
            "languages": "<string>",
            "countries": "<string>",
            "numberOfPages": "<string>",
            "releaseDate": "<string>"
        }
}
```
### Delete record
To delete a record use DELETE with the isbn number in the api path.
DELETE /books/{isbn}

### Query record
To query a record use GET with the isbn number in the api path
GET /books/{isbn}

