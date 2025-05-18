from langchain.prompts import PromptTemplate

# Prompt for JMeter test plan generation
GENERATE_JMX_PROMPT = PromptTemplate.from_template(
    "Generate a valid Apache JMeter .jmx XML test plan for load testing the endpoint:\n"
    "{url}\n\n"
    "Requirements:\n"
    "- {users} virtual users\n"
    "- Duration: {duration} seconds\n"
    "- Save results to: {output_file}\n"
    "- HTTP GET request\n"
    "- Include Thread Group, Sampler, and CSV Result Saver\n"
    "\nOutput only the raw XML content."
)