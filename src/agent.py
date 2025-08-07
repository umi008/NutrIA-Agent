import os
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools.calculation_tools import calculate_bmi, calculate_bmr, calculate_macros

# Load environment variables from .env file
dotenv.load_dotenv()

# Ensure the GOOGLE_API_KEY is set
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

def get_prompt_template(prompt_name: str) -> str:
    """
    Reads the content of a specified prompt file from the prompts directory.

    Args:
        prompt_name (str): The name of the prompt file (e.g., 'system_agent_prompt.md').

    Returns:
        str: The content of the prompt file.
    """
    prompt_path = os.path.join("prompts", prompt_name)
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Prompt file not found: {prompt_path}"

def create_agent():
    """
    Creates and configures the wellness plan agent.

    Returns:
        AgentExecutor: The configured agent executor.
    """
    # Initialize the language model
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

    # Load the system prompt
    system_prompt_content = get_prompt_template("system_agent_prompt.md")
    
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt_content),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # Define the tools
    tools = [calculate_bmi, calculate_bmr, calculate_macros]

    # Create the agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True
    )

    return agent_executor

if __name__ == '__main__':
    # This is for testing purposes
    agent_executor = create_agent()
    # Example invocation
    # response = agent_executor.invoke({"input": "I am 25 years old, 1.75m tall, and weigh 70kg. What is my BMI?"})
    # print(response)