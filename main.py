from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

import yaml
from dotenv import load_dotenv # for .env
import os

load_dotenv('secrets.env')

with open('config.yaml', 'r') as file:
    config_data = yaml.safe_load(file)


system_instruction = "You are a helpful trail guide assistant for Adventure Works, an outdoor gear company." \
"Help users with basic trail recommendations, safety tips," \
"and gear suggestions for hiking and outdoor activities. Keep responses informative but concise."


if __name__ == '__main__':
    deployment_name = config_data['deployment_name']
    endpoint = os.getenv("endpoint")
    api_key = os.getenv("api_key")
    agent_name = os.getenv("agent_name")

    project_client = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )

    agent = project_client.agents.create_version(
        agent_name=agent_name,
        definition=PromptAgentDefinition(
            model=deployment_name,  # Use Global Standard model
            instructions=system_instruction,
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")