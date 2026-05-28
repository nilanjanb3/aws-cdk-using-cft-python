# 1-Day Hands-On Roadmap to Kickstart AWS CDK with Python

Since you already know **Terraform** and **CloudFormation**, this roadmap is designed to help you **map what you know** into **AWS CDK thinking** quickly and practically.

---

## Goal for the Day

By the end of this 1-day path, you should be able to:

- Understand **what AWS CDK is** and how it differs from Terraform/CFT
- Build and deploy **real AWS infrastructure using Python**
- Learn **core CDK fundamentals**
- Explore **common use cases**
- Practice **CDK best practices**
- Read, modify, synthesize, diff, deploy, and destroy stacks confidently

---

## Lesson-by-Lesson Roadmap

## Lesson 1: CDK Mental Model for Terraform/CFT Users

**What you’ll learn**

- What CDK is and where it fits in AWS IaC
- How **CDK generates CloudFormation**
- Core concepts:
  - **App**
  - **Stack**
  - **Construct**
  - **Synth**
  - **Deploy**
- How CDK compares to:
  - Terraform modules/resources/state model
  - CloudFormation templates/stacks

**Hands-on**

- Install CDK CLI and Python project dependencies
- Initialize a new Python CDK app
- Explore generated files
- Run synth and inspect the CloudFormation output

**Outcome**

- You understand the **CDK execution model**
- You can navigate a Python CDK project

---

## Lesson 2: Bootstrap + First Stack Deployment

**What you’ll learn**

- Why CDK bootstrap is needed
- CDK deployment lifecycle
- Commands you’ll use daily:
  - `cdk bootstrap`
  - `cdk synth`
  - `cdk diff`
  - `cdk deploy`
  - `cdk destroy`

**Hands-on**

- Bootstrap your AWS environment
- Create a simple S3 bucket stack
- Run diff before deploy
- Deploy it
- Verify in AWS Console
- Destroy and recreate it

**Outcome**

- You complete your **first real CDK deployment**
- You build confidence with the core workflow

---

## Lesson 3: Constructs, L1/L2/L3, and Resource Modeling

**What you’ll learn**

- Construct levels:
  - **L1**: raw CloudFormation resources
  - **L2**: AWS-friendly abstractions
  - **L3**: patterns/architectures
- When to use each
- How CDK models relationships and defaults

**Hands-on**

- Create one bucket using **L1**
- Create another using **L2**
- Compare readability, defaults, and control
- Use a higher-level pattern if available

**Outcome**

- You understand how to choose the right **abstraction level**
- You see how CDK improves over raw templates

---

## Lesson 4: Parameters, Context, Config, and Environments

**What you’ll learn**

- Difference between:
  - hardcoded values
  - context values
  - environment variables
  - stack props
  - CloudFormation parameters
- Managing multiple environments like dev/test/prod
- Region/account awareness in CDK

**Hands-on**

- Pass configuration into your stack
- Make resource naming environment-specific
- Deploy same app to different logical environments
- Inspect how config changes affect synth output

**Outcome**

- You can make CDK apps **portable and reusable**
- You avoid hardcoding and start designing for real environments

---

## Lesson 5: IAM, Security, and Permissions in CDK

**What you’ll learn**

- IAM roles, managed policies, inline policies
- CDK permission helpers such as grants
- Security-first defaults and where you must be explicit
- Least privilege in CDK applications

**Hands-on**

- Create an IAM role for Lambda
- Grant S3 read or write access
- Add explicit policy statements where needed
- Review generated IAM in synthesized template

**Outcome**

- You understand how **security and permissions** are expressed in CDK
- You can wire resources together safely

---

## Lesson 6: Practical Use Case — S3 + Lambda + API

**What you’ll learn**

- A common AWS CDK use case: serverless application provisioning
- Packaging code assets with infrastructure
- Event-driven and API-driven patterns
- Resource integration in CDK

**Hands-on**

- Create:
  - S3 bucket
  - Lambda function
  - API endpoint
- Connect permissions and environment variables
- Deploy and test the endpoint

**Outcome**

- You build your first **practical mini-project**
- You see how CDK shines in app + infra workflows

---

## Lesson 7: Outputs, Cross-Stack References, and Reusable Constructs

**What you’ll learn**

- Stack outputs
- Referencing resources across stacks
- When to split stacks
- How to create your own reusable construct

**Hands-on**

- Move networking or storage into a separate stack
- Export/import values or use stack references
- Wrap a small repeated resource pattern into a custom construct

**Outcome**

- You learn to design **modular CDK apps**
- You start thinking in reusable building blocks

---

## Lesson 8: Testing, Diffing, and Safe Changes

**What you’ll learn**

- Why CDK testing matters
- Unit testing infrastructure definitions
- Snapshot vs assertion-style tests
- Using `cdk diff` as part of safe delivery

**Hands-on**

- Write a simple unit test for one resource property
- Change your stack intentionally
- Run diff and inspect impact before deploy
- Deploy only after validating changes

**Outcome**

- You gain a **safe iteration workflow**
- You learn how to avoid blind infrastructure changes

---

## Lesson 9: Best Practices from Day 1

**What you’ll learn**

- Recommended CDK project structure
- Naming conventions
- Separation of concerns
- Avoiding overly large stacks
- Reusable constructs over copy-paste
- Security defaults
- Tagging
- Environment strategy
- Version management and dependency hygiene

**Hands-on**

- Refactor your project structure
- Add tags
- Improve naming consistency
- Move repeated logic into helper functions or constructs
- Review stack for security and maintainability improvements

**Outcome**

- Your code looks more like **production-quality CDK**
- You learn habits worth keeping from the start

---

## Lesson 10: Capstone Wrap-Up

**What you’ll learn**

- How all pieces fit together in a realistic workflow
- End-to-end CDK lifecycle

**Hands-on**

- Build or refine a mini project that includes:
  - at least one stack
  - one reusable construct
  - IAM permissions
  - one serverless component
  - outputs
  - one test
- Run:
  - synth
  - diff
  - deploy
  - validate
  - destroy

**Outcome**

- You finish the day with a complete **working AWS CDK project in Python**
- You are ready for deeper topics like pipelines, custom constructs, multi-account deployment, and CI/CD

---

## Suggested Project Progression for the Day

To keep the day fully hands-on, build progressively instead of doing disconnected labs:

### Project Flow

1. Start with a **basic S3 bucket stack**
2. Add **config and environments**
3. Add **IAM role and policies**
4. Add **Lambda**
5. Add **API Gateway**
6. Split into **multiple stacks**
7. Add **outputs**
8. Add **tests**
9. Refactor into **reusable constructs**

This way, every lesson builds on the previous one.

---

## Key Concepts You Must Internalize by End of Day

- **CDK is code that synthesizes into CloudFormation**
- **Constructs are the core unit of composition**
- **L2 constructs are usually the sweet spot**
- **`cdk diff` is your safety net**
- **Bootstrap is mandatory for many workflows**
- **CDK helps encode patterns, not just define resources**
- **Good CDK is not just deployable, it is maintainable and reusable**

---

## Best Practices Embedded in This Roadmap

- Start with **small deployable stacks**
- Prefer **L2 constructs** unless you need lower-level control
- Always run **synth** and **diff** before deploy
- Avoid hardcoding account, region, and names
- Keep IAM permissions **least privilege**
- Refactor repeated infra into **custom constructs**
- Treat CDK code like **application code**
- Add at least basic **tests** from the beginning
- Destroy unused resources to avoid surprise cost

---

## What This Roadmap Covers

- **Fundamentals**
  - app, stack, construct, synth, deploy, bootstrap
- **Use cases**
  - storage, IAM, serverless API, modular stacks
- **Best practices**
  - structure, security, reuse, diffing, testing, env design

---

## End-of-Day Success Criteria

By the end of the day, you should be able to say:

- I can create a CDK app in Python
- I understand how CDK maps to CloudFormation
- I can deploy and update stacks safely
- I know how to structure CDK projects
- I can build a small real-world AWS use case
- I know the first set of best practices to follow