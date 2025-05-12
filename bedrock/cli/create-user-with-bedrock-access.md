# Create a IAM User With Access

---

### Create User For AWS BedRock Access Only For Foundation Models

1. Create a JSON file with the intended Access, name the file `iam-policy-bedrock.json`

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
		        "Sid": "AllowModelAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:CreateModelInvocationJob",
                "bedrock:ListFoundationModels"
            ],
            "Resource": "*"
        }
    ]
}
```

1. Execute the below AWS CLI command to create the policy

```bash
aws iam create-policy \
    --profile devops \
    --policy-name "dev-bedrock-allow-foundation-models" \
    --policy-document file://iam-policy-bedrock.json \
    --region ap-south-1
```

1. Copy the ARN from the above command’s output
2. Create a JSON file, name the file `iam-role-bedrock.json`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "bedrock.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

1. Execute the below AWS CLI command to create the policy

```bash
aws iam create-role \
    --profile devops \
    --role-name "dev-bedrock-allow-foundation-models" \
    --assume-role-policy-document file://iam-role-bedrock.json
```

1. Attach policy to the role

```bash
aws iam attach-role-policy \
    --profile devops \
    --role-name "dev-bedrock-allow-foundation-models" \
    --policy-arn "arn:aws:iam::<your-aws-account-id>:policy/dev-bedrock-allow-foundation-models"
```

1. Create an IAM user, and assign policy

```bash
aws iam create-user \
    --profile devops \
    --user-name "dev-cmn-bedrock-user"

aws iam attach-user-policy \
    --profile devops \
    --user-name "dev-cmn-bedrock-user" \
    --policy-arn "arn:aws:iam::<your-aws-account-id>:policy/dev-bedrock-allow-foundation-models"
    
aws iam create-access-key \
    --profile devops \
    --user-name "dev-cmn-bedrock-user"
```

 8. Copy and Save the credentials from the “create-access-key” command

1. Create an AWS Profile to aid use via CLI (if needed)

```bash
aws configure --profile tmp-bedrock
<enter access key id>
<enter access key secret>
<default region name>
json
```