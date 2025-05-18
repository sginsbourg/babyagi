import os
import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from prompts import GENERATE_JMX_PROMPT
from tools import run_jmeter, analyze_results

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🧠 Initializing LLM...")

# Load OpenAI API key from .env or environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("Missing OPENAI_API_KEY in environment or .env file")

# Initialize LLM - Fallback to gpt-3.5-turbo if GPT-4 access denied
try:
    llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_API_KEY)
except Exception as e:
    logger.warning("Failed to load GPT-4, falling back to gpt-3.5-turbo")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)

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

# Build chain: prompt → llm
chain: RunnableSequence = GENERATE_JMX_PROMPT | llm

# Loop through tasks
for task in task_queue:
    if task["done"]:
        continue

    print(f"\n[Task] {task['task']}")

    if task["task"] == "generate test plan":
        print("📝 Generating JMeter test plan...")
        try:
            response = chain.invoke(context)
            jmx_content = response.content.strip()

            # Basic validation for XML content
            if "<?xml" not in jmx_content[:50]:
                raise ValueError("Generated content is not valid XML.")

            with open("test.jmx", "w", encoding="utf-8") as f:
                f.write(jmx_content)

            print("✅ Test plan saved to test.jmx")
            task["done"] = True
        except Exception as e:
            logger.error(f"❌ Failed to generate test plan: {e}")
            break

    elif task["task"] == "run test":
        print("🚀 Running JMeter test...")
        try:
            result_file = run_jmeter()
            print(f"✅ Test completed. Results saved to {result_file}")
            task["done"] = True
        except Exception as e:
            logger.error(f"❌ Failed to run test: {e}")
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
        except FileNotFoundError:
            logger.error("❌ results.jtl not found. Did JMeter run successfully?")
        except Exception as e:
            logger.error(f"❌ Failed to analyze results: {e}")
            break

print("\n🏁 All tasks completed.")
