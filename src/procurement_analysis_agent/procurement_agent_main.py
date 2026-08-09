from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

import yaml
from dotenv import load_dotenv # for .env
import os
from pathlib import Path # for relative paths

BASE_DIR = Path(__file__).resolve().parent # regardless where to run parent of 'src' or inside 'src', relative to file path

load_dotenv(BASE_DIR / "secrets.env")

with open(BASE_DIR / "config.yaml", 'r') as file:
    config_data = yaml.safe_load(file)

with open(BASE_DIR / "prompts" / "v4_optimized_concise.txt") as fd:
    system_instruction = fd.read().strip()

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