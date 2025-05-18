import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from prompts import GENERATE_JMX_PROMPT
from tools import run_jmeter, analyze_results

print("🧠 Initializing LLM...")

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Task queue
task_queue = [
    {"id": 1, "task": "generate test plan", "done": False},
    {"id": 2, "task": "run test", "done": False},
    {"id": 3, "task": "analyze results", "done": False}
]

# Simulated user input
context = {
    "url": "https://example.com ",
    "users": 10,
    "duration": 60,
    "output_file": "results.jtl"
}

# Combine LLM + Prompt into a runnable chain
chain = llm | GENERATE_JMX_PROMPT

# Loop through tasks
for task in task_queue:
    if task["done"]:
        continue

    print(f"\n[Task] {task['task']}")

    if task["task"] == "generate test plan":
        print("📝 Generating JMeter test plan...")
        try:
            response = chain.invoke(context)
            with open("test.jmx", "w", encoding="utf-8") as f:
                f.write(response.content.strip())
            print("✅ Test plan saved to test.jmx")
            task["done"] = True
        except Exception as e:
            print(f"❌ Failed to generate test plan: {e}")
            break

    elif task["task"] == "run test":
        print("🚀 Running JMeter test...")
        try:
            result_file = run_jmeter()
            print(f"✅ Test completed. Results saved to {result_file}")
            task["done"] = True
        except Exception as e:
            print(f"❌ Failed to run test: {e}")
            break

    elif task["task"] == "analyze results":
        print("📊 Analyzing results...")
        try:
            stats = analyze_results()
            print("✅ Analysis complete.")
            print(f"Average Response Time: {stats['avg_response_time']:.2f} ms")
            print(f"Error Rate: {stats['error_rate'] * 100:.2f}%")
            print(f"Throughput: {stats['throughput']:.2f} req/sec")
            task["done"] = True
        except Exception as e:
            print(f"❌ Failed to analyze results: {e}")
            break

print("\n🏁 All tasks completed.")
