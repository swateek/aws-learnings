#!./.venv/bin/python3

"""Samples for using AWS BedRock"""

import json
import boto3
from tabulate import tabulate

from botocore.exceptions import ClientError

class SampleAWSBedrock:
    """SampleAWSBedrock"""

    def __init__(self):
        self.aws_profile = 'tmp-bedrock'
        self.session = boto3.Session(profile_name='tmp-bedrock')
        self.bedrock_client = self.session.client('bedrock')
        self.bedrock_runtime_client = self.session.client('bedrock-runtime')

    def list_all_foundation_models(self, provider):
        """list_all_foundation_models"""
        kwargs = {}
        if provider:
            kwargs['byProvider'] = provider
        response = self.bedrock_client.list_foundation_models(**kwargs)
        return response
    
    def readable_list_all_foundation_models(self, provider):
        """readable_list_all_foundation_models"""
        aws_response = self.list_all_foundation_models(provider)
        response = []

        for model in aws_response['modelSummaries']:
            itm = {}
            itm['providerName'] = model['providerName']
            itm['modelName'] = model['modelName']
            itm['modelId'] = model['modelId']
            itm['modelArn'] = model['modelArn']
            response.append(itm)

        return response
    
    def basic_version_invoke_model(self, model_id, request):
        """basic_version_invoke_model"""
        try:
            # Invoke the model with the request.
            response = self.bedrock_runtime_client.invoke_model(modelId=model_id, body=request)
            return response
        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
            exit(1)


    def run(self):
        """the basic run method"""
        # resp = self.list_all_foundation_models(None)
        # print(resp)
        # resp = self.readable_list_all_foundation_models('anthropic')
        # print(tabulate(resp, headers="keys"))
        # resp = self.readable_list_all_foundation_models('amazon')
        # print(tabulate(resp, headers="keys"))

        model_id = "amazon.titan-text-express-v1"
        prompt = "Describe the purpose of a 'hello world' program in one line."
        native_request = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0.5,
            },
        }
        request = json.dumps(native_request)
        response = self.basic_version_invoke_model(model_id, request)
        # Decode the response body.
        model_response = json.loads(response["body"].read())
        # Extract and print the response text.
        response_text = model_response["results"][0]["outputText"]
        print(response_text)

SampleAWSBedrock().run()
