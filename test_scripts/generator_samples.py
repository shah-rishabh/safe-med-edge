from llm.generator import generate
import json

test_queries = [
    "fever and headache",
    "chest pain and dizziness",
    "mild cough for 3 days",
    "I have fever, headache, fatigue, body ache, and mild cough for 4 days",
    "I feel weird and tired",
]

results = []

for q in test_queries:
    print(f"Query: {q}")
    output = generate(q)

    results.append({"query": q, **output})

with open("./logs/logs_day1_generator.json", "w") as f:
    json.dump(results, f, indent=4)
