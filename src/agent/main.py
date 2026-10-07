import os

from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel

from src.agent.prompts import SYSTEM_PROMPT
from src.tools.telemetry import analyze_latency


def create_agent() -> Agent:
    load_dotenv()

    region = os.getenv("AWS_REGION", "us-west-2")
    model_id = os.getenv("BEDROCK_MODEL_ID")

    if not model_id:
        raise RuntimeError(
            "BEDROCK_MODEL_ID is missing. Add it to your .env file."
        )

    model = BedrockModel(
        model_id=model_id,
        region_name=region,
    )

    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
	tools=[analyze_latency],
        callback_handler=None,
    )

def main() -> None:
    agent = create_agent()

    print("AI SRE Incident Investigator")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("incident> ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        response = agent(question)
        print(f"\n{response}\n")


if __name__ == "__main__":
    main()
