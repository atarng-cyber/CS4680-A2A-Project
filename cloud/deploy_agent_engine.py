# cloud/deploy_agent_engine.py
import os
import sys

import vertexai
from vertexai.preview import reasoning_engines

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from server.agent_engine_wrapper import EchoAgent  # noqa: E402

PROJECT_ID = 'cs4680-a2a-project'
REGION = 'us-central1'
STAGING = f'gs://{PROJECT_ID}-a2a-staging'

vertexai.init(project=PROJECT_ID, location=REGION, staging_bucket=STAGING)

remote_agent = reasoning_engines.ReasoningEngine.create(
    EchoAgent(),
    requirements=[
        'fastapi==0.111.0',
        'uvicorn==0.29.0',
        'pydantic==2.7.0',
        'google-cloud-aiplatform'
    ],
    extra_packages=['./server'],
    display_name='Echo A2A Agent',
    description='A2A Lab — Echo Agent on Agent Engine',
    gcs_dir_name=STAGING,
)

print('Deployed! Resource name:', remote_agent.resource_name)
print('Engine ID:', remote_agent.resource_name.split('/')[-1])
