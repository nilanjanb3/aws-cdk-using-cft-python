# CDK Bootstrap and Deployment Lifecycle

This lesson is about understanding **how CDK actually gets infrastructure into AWS** and why **bootstrap** is a required setup step in many cases.

Since you already know Terraform and CloudFormation, the easiest way to think about this is:

- **CDK** is the authoring layer
- **CloudFormation** is the deployment engine
- **Bootstrap** prepares your AWS account/region so CDK can deploy certain kinds of assets safely

---

## Why CDK Bootstrap Is Needed

**Bootstrap** means preparing an AWS environment so CDK can deploy resources properly.

When you run:

```bash
cdk bootstrap
```

CDK creates a special support stack in your AWS account and region, typically called something like:

```text
CDKToolkit
```

This stack creates resources that CDK may need during deployment, especially for:

- uploading **Lambda code bundles**
- storing **file assets**
- publishing **Docker image assets**
- managing deployment roles and permissions
- enabling modern CDK deployment workflows

### In simple words

Bootstrap is like **laying down the deployment plumbing** before your actual app stacks are deployed.

Without bootstrap, many CDK apps cannot deploy because CDK has nowhere to put packaged assets or may not have the expected support resources.

---

## What Bootstrap Usually Creates

Depending on your CDK version and setup, bootstrap commonly creates:

- an **S3 bucket**
  - used to store file assets such as Lambda zip packages
- **ECR repository support**
  - for container image assets
- IAM roles
  - deployment role
  - file publishing role
  - image publishing role
  - lookup role
- the **CDKToolkit** CloudFormation stack

You don’t usually manage these manually; CDK sets them up for you.

---

## Why This Is Different from Terraform Thinking

In Terraform, there is no exact equivalent to CDK bootstrap for normal operation. Terraform usually just uses:

- provider credentials
- backend configuration
- direct API operations

In CDK, because deployments often involve:

- synthesized CloudFormation templates
- asset publishing
- deployment roles

the environment needs some one-time setup.

So bootstrap is more of a **platform preparation step** for CDK deployments.

---

## When Bootstrap Is Required

You usually need bootstrap when:

- deploying CDK for the first time in an account/region
- using Lambda assets
- using Docker image assets
- using modern synthesis/deployment features
- deploying across environments or with advanced role-based setups

### Practical rule

If you are starting fresh, just assume:

- **bootstrap first**
- then **deploy**

That’s the safest mental model.

---

# CDK Deployment Lifecycle

Here’s the full lifecycle of how CDK works in practice.

## The Flow

1. You write CDK code in Python
2. CDK executes that code locally
3. CDK synthesizes CloudFormation templates
4. CDK compares local definition with deployed state
5. CDK uploads assets if needed
6. CloudFormation creates or updates the stack
7. You verify and iterate

---

## Lifecycle Explained Step by Step

## Step 1: Write Infrastructure in Code

You define infrastructure in Python using CDK constructs.

Example:

- S3 bucket
- Lambda
- API Gateway
- IAM roles

This is your source of truth.

---

## Step 2: Synthesize the App

CDK converts your code into CloudFormation templates.

This happens with:

```bash
cdk synth
```

Output goes to:

- terminal
- `cdk.out/` folder

This is your chance to inspect what will actually be handed to CloudFormation.

---

## Step 3: Compare Changes

Before applying anything, you check what’s going to change.

This happens with:

```bash
cdk diff
```

This is similar in spirit to Terraform plan.

It helps you see:

- new resources
- modified resources
- deleted resources
- policy changes
- security-sensitive differences

This should become a daily habit.

---

## Step 4: Deploy

Once changes look correct, you deploy with:

```bash
cdk deploy
```

At this point CDK:

- synthesizes templates
- publishes assets if needed
- submits the template to CloudFormation
- waits for stack creation or update

CloudFormation then performs the actual infrastructure changes.

---

## Step 5: Destroy When Done

To clean up resources, use:

```bash
cdk destroy
```

This tells CloudFormation to delete the stack and its managed resources.

This is especially useful during learning to avoid unnecessary AWS cost.

---

# Commands You’ll Use Daily

These are the core CDK commands you should get comfortable with immediately.

---

## `cdk bootstrap`

### What it does

Prepares an AWS account/region for CDK deployments by creating support infrastructure.

### Typical usage

```bash
cdk bootstrap
```

Or explicitly for an environment:

```bash
cdk bootstrap aws://ACCOUNT_ID/REGION
```

### Use it when

- first time using CDK in an account/region
- enabling deployment support for assets and roles

### What to remember

- usually a **one-time per account/region** task
- creates the **CDKToolkit** stack
- required for many real deployments

---

## `cdk synth`

### What it does

Generates CloudFormation templates from your CDK app.

### Typical usage

```bash
cdk synth
```

### Use it when

- checking what your code produces
- debugging resource definitions
- learning how constructs map to CloudFormation
- validating before deployment

### What to remember

- **always safe**
- does not create AWS resources
- helps you inspect generated output in `cdk.out`

---

## `cdk diff`

### What it does

Shows the difference between your current CDK app and the deployed stack.

### Typical usage

```bash
cdk diff
```

### Use it when

- before every deployment
- validating intended changes
- catching accidental IAM or destructive changes

### What to remember

- this is your **pre-deploy safety check**
- similar to Terraform plan in day-to-day workflow
- especially important when refactoring CDK code

---

## `cdk deploy`

### What it does

Deploys your synthesized stack to AWS via CloudFormation.

### Typical usage

```bash
cdk deploy
```

To deploy a specific stack:

```bash
cdk deploy MyStack
```

### Use it when

- you’ve reviewed synth/diff
- you’re ready to create or update infrastructure

### What to remember

- CDK may package and upload assets first
- CloudFormation performs the actual create/update
- this is the command that changes AWS resources

---

## `cdk destroy`

### What it does

Deletes the deployed stack and its managed resources.

### Typical usage

```bash
cdk destroy
```

To destroy a specific stack:

```bash
cdk destroy MyStack
```

### Use it when

- cleaning up lab resources
- removing unused stacks
- avoiding cost during learning

### What to remember

- some resources may block deletion depending on retention settings or non-empty state
- always verify what is being deleted

---

# Recommended Daily Workflow

For hands-on CDK work, this should become your standard loop:

1. Change CDK Python code
2. Run `cdk synth`
3. Run `cdk diff`
4. Run `cdk deploy`
5. Validate in AWS
6. Run `cdk destroy` when finished with temporary resources

This is the practical workflow you’ll repeat constantly.

---

# Mental Mapping to Terraform

Here’s the closest day-to-day mapping:

| Terraform | CDK |
|---|---|
| `terraform init` | `cdk bootstrap` |
| `terraform plan` | `cdk diff` |
| `terraform apply` | `cdk deploy` |
| `terraform destroy` | `cdk destroy` |
| HCL rendering/config | `cdk synth` |

### Important caveat

This mapping is helpful, but not exact:

- `terraform init` mainly sets up providers/backend
- `cdk bootstrap` creates real AWS support infrastructure

So they are similar in workflow position, but not functionally identical.

---

# Mental Mapping to CloudFormation

| CloudFormation World | CDK World |
|---|---|
| Write template | Write Python CDK code |
| Validate template | `cdk synth` |
| Review stack changes | `cdk diff` |
| Create/update stack | `cdk deploy` |
| Delete stack | `cdk destroy` |

This is why CDK feels operationally very familiar if you know CloudFormation.

---

# Most Important Takeaways

## Bootstrap

- prepares your AWS environment for CDK
- often required before first deploy
- creates support resources in the `CDKToolkit` stack

## Synth

- turns Python code into CloudFormation
- safe and inspectable
- useful for learning and debugging

## Diff

- shows intended infrastructure changes
- should be run before deploy
- helps prevent surprises

## Deploy

- applies changes via CloudFormation
- creates or updates AWS resources
- may publish assets first

## Destroy

- removes the stack
- useful for cost control and cleanup
- part of normal learning workflow

---

# Short Practical Summary

If you want the simplest possible mental model:

- **bootstrap** = prepare the environment
- **synth** = generate CloudFormation
- **diff** = preview changes
- **deploy** = apply changes
- **destroy** = clean up

---

# What You Should Internalize Before the Next Lesson

- CDK does not skip CloudFormation; it uses it
- Bootstrap is foundational for many real deployments
- `cdk diff` should become a habit
- The safest workflow is:
  - **synth**
  - **diff**
  - **deploy**
- `destroy` is part of responsible learning in AWS