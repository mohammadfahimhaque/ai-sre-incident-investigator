import os

from dotenv import load_dotenv
from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.models import BedrockModel

from src.agent.prompts import SYSTEM_PROMPT
from src.tools.mcp import create_bronto_mcp_client
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

    bronto_mcp = create_bronto_mcp_client()

    conversation_manager = SlidingWindowConversationManager(
        window_size=8,
        should_truncate_results=True,
        per_turn=True,
        proactive_compression={
            "compression_threshold": 0.65,
        },
    )

    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[
            analyze_latency,
            bronto_mcp,
        ],
        conversation_manager=conversation_manager,
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

        try:
            response = agent(question)
            print(f"\n{response}\n")
        except KeyboardInterrupt:
            print("\nInvestigation cancelled.\n")
        except Exception as exc:
            print(f"\nInvestigation failed: {exc}\n")


if __name__ == "__main__":
    main()
