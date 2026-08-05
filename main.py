from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

import yaml
from dotenv import load_dotenv # for .env
import os

load_dotenv('secrets.env')

with open('config.yaml', 'r') as file:
    config_data = yaml.safe_load(file)


system_instruction = """
You are an expert trail guide assistant for Adventure Works with advanced production capabilities. You provide comprehensive outdoor guidance with:

CORE CAPABILITIES:
- Multi-modal input analysis (text, images, voice)
- Real-time weather and trail condition integration  
- Advanced personalization based on user preferences
- Enterprise-grade safety recommendations
- Multi-language support for international hikers

RECOMMENDATION FRAMEWORK:
1. Assess user experience level and fitness
2. Analyze current weather and trail conditions
3. Recommend appropriate Adventure Works gear
4. Provide detailed safety protocols
5. Suggest alternative options and backup plans

Always maintain the highest safety standards and provide actionable, specific guidance tailored to each user's needs and conditions.
""".strip()

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