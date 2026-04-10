import os
import requests
from dotenv import load_dotenv
import argparse

from datamodels.generator_models import ModelResponse
from prompts.system_prompt import system_prompt

# Load .env
load_dotenv()

# Set env vars
OLLAMA_URL: str = os.getenv("OLLAMA_URL")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL")


def generate(prompt: str):
    payload = {
        "model": OLLAMA_MODEL,
        "system": system_prompt,
        "prompt": prompt,
        "think": False,
        "format": ModelResponse.model_json_schema(),
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload)
    result = response.json()

    tokens = result.get("eval_count", None)

    latency = result.get("total_duration", None)
    if latency:
        latency = round(float(latency) / 10**9, 2)

    tps = round(tokens / latency, 2) if (tokens and latency) else None

    return {
        "response": result["response"],
        "latency": latency,
        "tokens": tokens,
        "tps": tps,
    }


def main():
    parser = argparse.ArgumentParser(description="Medical AI Generator Tool")

    parser.add_argument("query", type=str, help="The medical symptom to analyze")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print out the Metrics or not"
    )

    args = parser.parse_args()

    output = generate(args.query)

    print("\n=== RESPONSE ===")
    print(output["response"])

    if args.verbose:
        print("\n=== METRICS ===")
        print(f"Latency: {output['latency']}s")
        print(f"Tokens: {output['tokens']}")
        print(f"Tokens per Second: {output['tps']}")


if __name__ == "__main__":
    main()
