import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_python_demo.cdk_python_demo_stack import CdkPythonDemoStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_python_demo/cdk_python_demo_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkPythonDemoStack(app, "cdk-python-demo")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
