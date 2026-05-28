# AWS CDK Fundamentals for a Terraform/CFT User

Since you’ve already used **Terraform** and **CloudFormation**, the fastest way to understand CDK is to see it as **an infrastructure programming layer on top of CloudFormation**.

---

## What AWS CDK Is and Where It Fits in AWS IaC

**AWS CDK** stands for **Cloud Development Kit**. It lets you define AWS infrastructure using a programming language like **Python**, **TypeScript**, **Java**, or **C#**, instead of writing raw YAML or JSON templates.

At a high level, CDK sits like this:

- **Your Python code**
- becomes **CDK constructs and stacks**
- which are **synthesized into CloudFormation templates**
- which are then deployed by **CloudFormation** into AWS

So CDK is **not replacing CloudFormation under the hood**. It is a **higher-level developer-friendly way to produce CloudFormation**.

### Where it fits in AWS IaC

You can think of the AWS IaC options roughly like this:

| Tool | What you write | What actually deploys |
|---|---|---|
| CloudFormation | YAML/JSON template | CloudFormation |
| AWS CDK | Python/TypeScript/etc. | CloudFormation |
| Terraform | HCL | Terraform engine/providers |

So:

- **CloudFormation** = direct template-based AWS IaC
- **CDK** = code-first abstraction that compiles to CloudFormation
- **Terraform** = separate IaC engine with its own state model and provider ecosystem

---

## How CDK Generates CloudFormation

This is the key mental model.

When you write CDK in Python, you are **not directly creating AWS resources at Python runtime**. Your Python code is used to **describe infrastructure**, and then CDK converts that description into a CloudFormation template.

That conversion step is called **synthesis**.

### Flow

1. You write Python CDK code
2. CDK executes that code locally
3. CDK builds an in-memory construct tree
4. CDK converts the construct definitions into a CloudFormation template
5. CloudFormation deploys the resulting template into AWS

### Important implication

CDK code runs in **two different realities**:

- **At synth time**
  - Python executes locally on your machine or CI runner
- **At deploy time**
  - CloudFormation creates AWS resources in your account

That means:

- normal Python logic can help you **generate infrastructure definitions**
- but Python code itself does **not keep running in AWS** unless you package it as something like Lambda

---

## Core Concepts

## App

An **App** is the **top-level container** in a CDK project.

It is the root object that holds one or more stacks.

Think of it as:

- the entry point of your CDK program
- the overall deployment application
- the parent of all stacks and constructs

### Mental mapping

- In a CDK project, `app.py` usually creates the **App**
- Then the app creates one or more **Stacks**

You can think of the app like the **root execution context** of your infrastructure program.

---

## Stack

A **Stack** is a unit of deployment that maps to a **CloudFormation stack**.

This is one of the most important things to remember:

- **One CDK Stack = One CloudFormation Stack**

A stack contains AWS resources such as:

- S3 buckets
- Lambda functions
- VPCs
- IAM roles
- DynamoDB tables

### Why stacks matter

Stacks give you:

- a deployment boundary
- a lifecycle boundary
- an update boundary
- a logical grouping of resources

### Example grouping

You might have:

- `NetworkStack`
- `AppStack`
- `MonitoringStack`

Each would synthesize into a separate CloudFormation stack.

---

## Construct

A **Construct** is the basic building block in CDK.

Everything in CDK is built from constructs.

A construct can represent:

- a single AWS resource
  - like an S3 bucket
- a higher-level AWS abstraction
  - like a Lambda function with log retention and permissions
- a reusable custom component
  - like your own “serverless API service” building block

### Think of constructs like this

If CloudFormation is made of **resource definitions**, CDK is made of **constructs**.

Constructs are composable and hierarchical.

A stack contains constructs, and constructs can contain child constructs.

### Construct levels

You’ll often hear these:

- **L1 Constructs**
  - raw CloudFormation-level resources
  - closest to the underlying template
- **L2 Constructs**
  - higher-level AWS-friendly abstractions
  - most common in day-to-day CDK use
- **L3 Constructs**
  - patterns composed from multiple resources
  - opinionated reusable architecture blocks

For a Terraform user, L2/L3 often feel like using **well-designed modules with defaults and relationships built in**.

---

## Synth

**Synth** means **synthesize**.

This is the process where CDK turns your code into a CloudFormation template.

When you run:

```bash
cdk synth
```

CDK:

- executes your Python code
- resolves construct definitions
- generates one or more CloudFormation templates
- writes them to the `cdk.out` directory

### Why synth matters

It lets you inspect what CDK is actually going to hand over to CloudFormation.

This is very important because CDK can feel magical at first. `cdk synth` helps you verify:

- what resources are being created
- what logical IDs were generated
- what IAM policies exist
- what defaults CDK added for you

For learning CDK, **always inspect synth output**.

---

## Deploy

**Deploy** means taking the synthesized CloudFormation and asking AWS to apply it.

When you run:

```bash
cdk deploy
```

CDK generally:

- synthesizes the app
- compares changes
- submits the CloudFormation stack
- waits for AWS to create or update resources

### Important point

CDK itself is **not the final deployer of AWS resources**. CloudFormation is still the deployment engine.

CDK is more like:

- authoring layer
- packaging layer
- orchestration CLI for CloudFormation-based deployment

---

# How CDK Compares to Terraform

For someone coming from Terraform, this comparison is the fastest path to intuition.

## CDK vs Terraform: Concept Mapping

| Terraform | AWS CDK |
|---|---|
| HCL code | Python/TypeScript/etc. code |
| Resource | Construct/resource definition |
| Module | Custom construct or stack composition |
| Plan | `cdk diff` plus CloudFormation change awareness |
| Apply | `cdk deploy` |
| State file | CloudFormation stack state |
| Provider | AWS construct libraries backed by CloudFormation |
| Variables | Context, env vars, stack props, parameters |
| Output | CloudFormation outputs / CDK outputs |

---

## Terraform Modules vs CDK Constructs

In Terraform, you use **modules** to create reusable infrastructure building blocks.

In CDK, the closest equivalent is a **custom construct**.

### Example intuition

If in Terraform you had a module for:

- S3 bucket
- IAM policy
- event notifications
- encryption defaults

In CDK, you would likely make a **construct** that encapsulates all of that in Python.

### Difference in feel

- Terraform modules are mostly **declarative composition**
- CDK constructs are **programmable composition**

That means in CDK you can use:

- loops
- conditionals
- functions
- classes
- abstraction patterns from software engineering

This is powerful, but it also means you need discipline to keep infrastructure code readable.

---

## Terraform Resources vs CDK Resource Definitions

Terraform resources feel closer to:

- “define this infrastructure block”

CDK constructs often feel like:

- “instantiate this infrastructure object”

For example, in CDK you may write Python code that feels object-oriented, but the outcome is still infrastructure definition, not imperative provisioning.

So although the syntax feels more dynamic, the goal remains declarative infrastructure through CloudFormation.

---

## Terraform State vs CDK/CloudFormation State

This is a major difference.

### Terraform

Terraform keeps a **state file** that tracks real-world resources and desired configuration.

That state file is central to Terraform behavior.

### CDK

CDK itself does **not maintain a separate infrastructure state file like Terraform**.

Instead:

- CloudFormation tracks the deployed stack state
- CDK generates templates and asks CloudFormation to reconcile them

### Practical meaning

With CDK:

- you rely on CloudFormation stack state
- drift handling is CloudFormation-style, not Terraform-style
- updates happen through stack updates, not state reconciliation using a local or remote `.tfstate`

This is why CDK feels much closer to CloudFormation operationally than Terraform, even though the authoring experience is code-first.

---

## Terraform Plan vs CDK Diff

Terraform gives you `terraform plan`.

CDK gives you `cdk diff`.

They are similar in spirit, but not identical.

### Terraform plan

- compares desired config with state and provider reality
- produces a detailed execution plan

### CDK diff

- compares synthesized CloudFormation against deployed stack/template state
- shows what is expected to change before deployment

So `cdk diff` is your “sanity check before apply,” but the underlying mechanism is different because CloudFormation is the deployment engine.

---

# How CDK Compares to CloudFormation

This comparison is even more direct.

## CDK vs CloudFormation: Concept Mapping

| CloudFormation | AWS CDK |
|---|---|
| Template | Synthesized output from CDK |
| Stack | CDK Stack |
| Resource in YAML/JSON | Construct/resource in code |
| Parameters | Stack props, context, env vars, or CFN parameters |
| Outputs | CDK outputs |
| Nested stacks | Nested stacks / composition in CDK |
| Deploy via CFN | Deploy via CDK CLI backed by CFN |

---

## CloudFormation Templates vs CDK Code

In raw CloudFormation, you write the infrastructure definition directly in YAML or JSON.

In CDK, you write code that **generates** that definition.

That means CDK gives you:

- abstraction
- reuse
- loops
- conditional generation
- composition
- cleaner refactoring

Instead of manually repeating similar template sections, you can encapsulate patterns as Python classes and functions.

---

## CloudFormation Stacks vs CDK Stacks

This mapping is almost one-to-one:

- **CDK Stack = CloudFormation Stack**

So if you already understand:

- stack creation
- stack update
- stack deletion
- stack outputs
- stack dependencies

then you already understand a big part of CDK runtime behavior.

What changes is mostly the **authoring model**, not the deployment engine.

---

# The Most Important Mental Model

If you remember only one thing, remember this:

**AWS CDK is a programming interface for defining CloudFormation stacks.**

Or even shorter:

**CDK = code that synthesizes into CloudFormation.**

That single idea explains:

- why synth exists
- why deploy uses CloudFormation
- why stacks map to CloudFormation stacks
- why constructs are abstractions over AWS resources
- why CDK feels more expressive than raw templates

---

# Practical Summary for You

Because you know Terraform and CloudFormation already, here’s the fastest translation:

- If **CloudFormation** feels too verbose, CDK fixes the authoring experience
- If **Terraform modules** feel reusable, CDK constructs give similar reuse with more programming power
- If you expect a Terraform-style **state file**, CDK does not work that way
- If you already understand **CloudFormation stacks**, you already understand CDK deployment behavior pretty well

---

# Cheat Sheet

| Concept | Meaning |
|---|---|
| **App** | Top-level CDK program container |
| **Stack** | Deployable unit, maps to a CloudFormation stack |
| **Construct** | Building block of CDK, from resources to reusable patterns |
| **Synth** | Convert CDK code into CloudFormation template |
| **Deploy** | Send synthesized stack to CloudFormation for creation/update |

---

# What You Should Internalize Before Moving On

- **CDK is not “AWS resources created directly by Python”**
- **Python is used to define infrastructure**
- **CloudFormation still performs the actual deployment**
- **Constructs are the core abstraction**
- **Stacks are deployment boundaries**
- **Synth is the bridge from code to template**
- **Deploy is CloudFormation execution**