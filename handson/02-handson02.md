# Hands-On: Bootstrap, Deploy, Verify, Destroy, and Recreate an S3 Bucket Stack

This exercise will take you through the full basic AWS CDK workflow using **Python**:

- bootstrap the environment
- create a simple stack
- preview changes
- deploy
- verify in AWS
- destroy
- recreate

This is the best first deployment loop to build confidence 🙂  

---

## What You’ll Do

By the end, you will have used these commands in a real flow:

- `cdk bootstrap`
- `cdk synth`
- `cdk diff`
- `cdk deploy`
- `cdk destroy`

---

## Prerequisites

You should already have:

- AWS CLI configured
- CDK CLI installed
- Python virtual environment set up
- a CDK Python app initialized

If you’re in your existing project folder, activate your virtual environment first.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

---

## Step 1: Confirm AWS Identity and Region

Before bootstrapping, verify which AWS account and region you are using.

Run:

```bash
aws sts get-caller-identity
aws configure list
```

You want to know:

- your **Account ID**
- your **active region**

If region is not configured, you can set one like this:

```bash
aws configure
```

Or export it temporarily:

### macOS / Linux

```bash
export AWS_DEFAULT_REGION=us-east-1
```

### Windows PowerShell

```powershell
$env:AWS_DEFAULT_REGION="us-east-1"
```

---

## Step 2: Bootstrap Your AWS Environment

Now bootstrap the target account and region.

### Option A: Simple bootstrap

```bash
cdk bootstrap
```

### Option B: Explicit account and region

Replace with your real values:

```bash
cdk bootstrap aws://123456789012/us-east-1
```

### What this does

It creates a support stack, usually named:

```text
CDKToolkit
```

This stack helps CDK manage deployment assets and roles.

### What success looks like

You should see output showing:

- stack creation started
- resources being created
- bootstrap complete

---

## Step 3: Add a Simple S3 Bucket to Your Stack

Open your stack file, likely something like:

```text
cdk_python_demo/cdk_python_demo_stack.py
```

Replace it with this minimal stack:

```python
from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
)
from constructs import Construct


class CdkPythonDemoStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3.Bucket(
            self,
            "MyFirstBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
```

---

## Why These Settings Matter

### `versioned=True`

This enables S3 bucket versioning so you can see a real bucket property in action.

### `removal_policy=RemovalPolicy.DESTROY`

This tells CDK/CloudFormation to delete the bucket when the stack is destroyed.

### `auto_delete_objects=True`

This helps empty the bucket automatically before deletion.

Without this, destroying the stack may fail if the bucket contains objects.

---

## Step 4: Synthesize the Stack

Before diff or deploy, generate the CloudFormation template.

```bash
cdk synth
```

This lets you confirm the stack is valid.

You should see a generated template containing an S3 bucket resource.

---

## Step 5: Run Diff Before Deploy

Now preview what CDK wants to change:

```bash
cdk diff
```

### What you should expect

Since the stack is not deployed yet, you’ll usually see:

- a new S3 bucket resource
- possibly a custom resource for object auto-delete
- IAM-related resources if needed for cleanup support

### Why this matters

This is your safety habit:

- change code
- run synth
- run diff
- only then deploy

---

## Step 6: Deploy the Stack

Now deploy:

```bash
cdk deploy
```

If prompted for approval, confirm.

### What CDK will do

- synthesize the app
- package any needed assets
- submit the template to CloudFormation
- create the stack resources

### What success looks like

At the end, you should see:

- stack status complete
- stack outputs if any
- deployment success message

---

## Step 7: Verify in AWS Console

Now verify that the stack and bucket were really created.

### Check in CloudFormation Console

Go to:

- AWS Console
- CloudFormation
- Stacks

Look for your stack, likely named:

```text
CdkPythonDemoStack
```

Open it and inspect:

- status
- resources tab
- template tab
- events tab

### Check in S3 Console

Go to:

- AWS Console
- S3

Look for the bucket CDK created.

Note:

- the physical bucket name is usually auto-generated
- it may not be exactly `MyFirstBucket`
- `MyFirstBucket` is the CDK construct ID, not necessarily the actual S3 bucket name

### What to verify

In S3:

- bucket exists
- versioning is enabled

In CloudFormation:

- stack status is `CREATE_COMPLETE`

---

## Step 8: Destroy the Stack

Now clean everything up:

```bash
cdk destroy
```

Confirm when prompted.

### What should happen

CloudFormation will:

- delete helper resources
- empty and delete the bucket
- remove the stack

### Verify deletion

Check CloudFormation again:

- stack should disappear after deletion completes

Check S3 again:

- bucket should be gone

---

## Step 9: Recreate the Stack

Now deploy it again from the same code.

First preview:

```bash
cdk diff
```

Then deploy:

```bash
cdk deploy
```

This confirms your setup is repeatable.

That repeatability is the whole point of IaC.

---

## Full Command Flow

Here’s the complete command sequence in one place.

```bash
aws sts get-caller-identity
aws configure list
cdk bootstrap
cdk synth
cdk diff
cdk deploy
cdk destroy
cdk diff
cdk deploy
```

---

## Recommended Verification Checklist

After first deploy, confirm all of these:

- **Bootstrap stack exists**
  - `CDKToolkit` in CloudFormation
- **Application stack exists**
  - your CDK stack in CloudFormation
- **S3 bucket exists**
  - visible in S3 Console
- **Versioning is enabled**
  - check bucket properties/settings
- **Destroy works cleanly**
  - stack deleted successfully
- **Recreate works**
  - second deploy succeeds

---

## What You’re Learning Under the Hood

This one exercise teaches several important CDK realities:

### Bootstrap is account/region setup

It prepares the environment for deployment.

### CDK code becomes CloudFormation

`cdk synth` proves this.

### Diff is your safety net

`cdk diff` helps you review intended changes before touching AWS.

### Deploy is CloudFormation-backed

CDK orchestrates, but CloudFormation executes.

### Destroy matters

Deleting resources safely is part of real IaC practice, not an afterthought.

---

## Common Issues You Might Hit

## Bootstrap fails

Possible reasons:

- wrong AWS credentials
- missing permissions
- invalid region
- account access restrictions

## Deploy fails because bucket name already exists

This usually happens only if you manually specify a globally unique bucket name. In the example above, CDK auto-generates one, so this is less likely.

## Destroy fails because bucket is not empty

This is exactly why we included:

```python
auto_delete_objects=True
```

and

```python
removal_policy=RemovalPolicy.DESTROY
```

## Region confusion

Make sure the AWS Console region matches the region you used for bootstrap and deploy.

---

## What You Should Internalize After This Exercise

By doing this once end-to-end, you should now understand:

- how to bootstrap an AWS environment for CDK
- how to define a simple resource in Python CDK
- how to synthesize and inspect the result
- how to preview changes with `cdk diff`
- how to deploy with confidence
- how to verify the stack in AWS Console
- how to destroy and recreate infrastructure cleanly

---

## Success Criteria

You’ve completed this hands-on successfully if:

- `cdk bootstrap` completed successfully
- `cdk deploy` created the bucket
- you verified the stack in CloudFormation
- you verified the bucket in S3
- `cdk destroy` removed everything cleanly
- `cdk deploy` worked again after destruction