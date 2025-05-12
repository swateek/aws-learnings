#!./.venv/bin/python3

"""Samples for using AWS BedRock"""

import boto3
from tabulate import tabulate

class SampleAWSBedrock:
    """SampleAWSBedrock"""

    def __init__(self):
        self.aws_profile = 'tmp-bedrock'
        self.session = boto3.Session(profile_name='tmp-bedrock')
        self.client = self.session.client('bedrock')

    def list_all_foundation_models(self, provider):
        """list_all_foundation_models"""
        kwargs = {}
        if provider:
            kwargs['byProvider'] = provider
        response = self.client.list_foundation_models(**kwargs)
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

    def run(self):
        """the basic run method"""
        # resp = self.list_all_foundation_models(None)
        # print(resp)
        resp = self.readable_list_all_foundation_models('anthropic')
        print(tabulate(resp, headers="keys"))

SampleAWSBedrock().run()
