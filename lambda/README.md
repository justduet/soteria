# Soteria

This is the lambda function for Soteria that hashes uploaded images and
updates the database with the hash

## Create zip file to upload to AWS Lambda

This zip is uploading python code to AWS lambda so it can be run from Lambda.

```bash
zip -r [file.zip] [files to add]


zip -r upload.zip lambda_function.py lib
```