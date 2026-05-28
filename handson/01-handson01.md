# Hands-On: Set Up AWS CDK with Python and Inspect `synth`

This lesson is about getting your **first CDK Python project running locally** and understanding what CDK generates behind the scenes.

---

## What You’ll Do

You will:

- Install the **AWS CDK CLI**
- Create a **new Python CDK project**
- Install project dependencies
- Explore the generated project files
- Run `cdk synth`
- Inspect the generated **CloudFormation template**

---

## Prerequisites

Make sure you already have:

- **Python 3.9+**
- **Node.js**
- **npm**
- **AWS CLI**
- AWS credentials configured with `aws configure`

You can quickly verify:

```bash
python3 --version
node --version
npm --version
aws --version
```

---

## Step 1: Install AWS CDK CLI

The CDK CLI is installed using npm.

```bash
npm install -g aws-cdk
```

Verify installation:

```bash
cdk --version
```

If this prints a version, you’re ready.

---

## Step 2: Create a New Project Folder

Make a fresh directory and move into it:

```bash
mkdir cdk-python-demo
cd cdk-python-demo
```

---

## Step 3: Initialize a New Python CDK App

Run:

```bash
cdk init app --language python
```

This generates a starter Python CDK project.

---

## Step 4: Create and Activate a Virtual Environment

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

After activation, your shell should show the virtual environment name.

---

## Step 5: Install Python Dependencies

The generated project usually contains a `requirements.txt` file.

Install dependencies with:

```bash
pip install -r requirements.txt
```

If the project also has dev requirements, install them too:

```bash
pip install -r requirements-dev.txt
```

---

## Step 6: Explore the Generated Files

After initialization, you’ll see a structure similar to this:

```text
cdk-python-demo/
├── app.py
├── cdk.json
├── requirements.txt
├── requirements-dev.txt
├── source.bat
├── README.md
├── tests/
└── cdk_python_demo/
    ├── __init__.py
    └── cdk_python_demo_stack.py
```

Here’s what matters most:

| File/Folder | Purpose |
|---|---|
| `app.py` | Entry point of the CDK app |
| `cdk.json` | CDK app configuration |
| `requirements.txt` | Python runtime dependencies |
| `requirements-dev.txt` | Dev/test dependencies |
| `tests/` | Unit tests for infrastructure |
| `cdk_python_demo_stack.py` | Your first stack definition |

---

## Step 7: Understand the Important Files

## `app.py`

This is the root of your CDK app. It usually:

- creates a CDK `App`
- instantiates one or more `Stack`s
- connects everything together

Typical starter content looks like this:

```python
#!/usr/bin/env python3
import aws_cdk as cdk

from cdk_python_demo.cdk_python_demo_stack import CdkPythonDemoStack

app = cdk.App()
CdkPythonDemoStack(app, "CdkPythonDemoStack")

app.synth()
```

### What this means

- `cdk.App()` creates the top-level app
- `CdkPythonDemoStack(...)` creates a stack inside the app
- `app.synth()` tells CDK to synthesize the app into CloudFormation

---

## `cdk_python_demo_stack.py`

This is where your infrastructure is defined.

Starter code often looks like:

```python
from aws_cdk import Stack
from constructs import Construct

class CdkPythonDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define resources here
```

### What this means

- your class extends `Stack`
- the constructor is where you define AWS resources
- currently, the generated stack may have no actual resources yet

---

## `cdk.json`

This tells CDK how to run your app.

Example:

```json
{
  "app": "python3 app.py",
  "watch": {
    "include": ["**"],
    "exclude": [
      "README.md",
      "cdk*.json",
      "requirements*.txt",
      "source.bat",
      "**/__init__.py",
      "**/__pycache__",
      "tests"
    ]
  }
}
```

Most important part:

- `"app": "python3 app.py"`

That is the command CDK runs when you execute `cdk synth` or `cdk deploy`.

---

## Step 8: Run `cdk synth`

Now run:

```bash
cdk synth
```

This is your first big CDK moment.

### What happens here

CDK will:

- execute `app.py`
- build the construct tree
- convert stack definitions into CloudFormation
- print the generated CloudFormation template to your terminal

It will also usually write output into the `cdk.out/` directory.

---

## Step 9: Inspect the `cdk.out` Folder

After synth, list the files:

```bash
ls cdk.out
```

You should see generated artifacts such as:

- CloudFormation template JSON
- manifest files
- asset metadata

Typical contents may look like:

```text
cdk.out/
├── CdkPythonDemoStack.template.json
├── manifest.json
├── tree.json
└── cdk.out
```

---

## Step 10: Inspect the Generated CloudFormation Template

Open the template file:

```bash
cat cdk.out/CdkPythonDemoStack.template.json
```

Or if you prefer better formatting:

```bash
python -m json.tool cdk.out/CdkPythonDemoStack.template.json
```

### What to look for

Even if your stack has no resources yet, inspect:

- `Resources`
- `Outputs`
- `Parameters`
- `Conditions`
- `Rules`

If the starter stack is empty, `Resources` may be empty or minimal.

That is fine. The point is to see that **CDK code becomes a CloudFormation template**.

---

## Step 11: Add One Tiny Resource for Better Learning

To make synth more meaningful, add a simple S3 bucket.

Edit `cdk_python_demo_stack.py`:

```python
from aws_cdk import (
    Stack,
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
        )
```

Now run:

```bash
cdk synth
```

---

## Step 12: Inspect What CDK Generated

Now check the synthesized template again:

```bash
python -m json.tool cdk.out/CdkPythonDemoStack.template.json
```

You should see a CloudFormation resource similar to an `AWS::S3::Bucket`.

### Key observation

You wrote:

```python
s3.Bucket(...)
```

But CDK generated:

- a CloudFormation template
- with an S3 bucket resource
- plus possible metadata or supporting configuration

This is the exact bridge between **CDK code** and **CloudFormation output**.

---

## What You Should Notice in the Synthesized Output

When inspecting the template, focus on these ideas:

### Resource translation

Your Python construct becomes a CloudFormation resource type such as:

- `AWS::S3::Bucket`

### Generated logical IDs

CDK creates logical IDs for resources automatically.

These may look different from your construct name, because CDK adds deterministic naming logic.

### Defaults added by CDK

CDK sometimes adds sensible defaults or metadata, depending on the construct.

This is one reason L2 constructs feel easier than raw CloudFormation.

---

## Mental Model to Lock In

When you run `cdk synth`, think:

- Python runs locally
- CDK builds infrastructure definitions
- output becomes CloudFormation
- CloudFormation is what AWS will deploy

That is the core of CDK.

---

## Mini Checklist for This Lesson

By the end of this hands-on step, you should have done all of these:

- Installed `aws-cdk` CLI
- Created a Python CDK project
- Activated a virtual environment
- Installed dependencies
- Opened and understood `app.py`
- Opened and understood the stack file
- Run `cdk synth`
- Opened the generated template in `cdk.out`
- Added a simple S3 bucket
- Confirmed that CDK generated CloudFormation from Python code

---

## Common Beginner Mistakes

- **Forgetting to activate the virtual environment**
  - then imports may fail
- **Not installing dependencies from `requirements.txt`**
  - synth will break on missing modules
- **Thinking CDK deploys directly from Python objects**
  - it actually synthesizes to CloudFormation first
- **Ignoring `cdk.out`**
  - this folder is extremely useful for learning and debugging

---

## Expected Outcome

At this point, you should be comfortable with:

- starting a CDK Python project
- locating the main project files
- understanding the role of `app.py` and the stack file
- using `cdk synth`
- seeing real CloudFormation generated from your Python code

---

## Your Next Learning Bridge

After this, the natural next step is:

- understanding **constructs**
- learning **L1 vs L2 vs L3**
- then doing your **first deploy**