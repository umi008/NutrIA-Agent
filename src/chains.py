from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.agent import get_prompt_template

def get_llm():
    """Initializes and returns a ChatGoogleGenerativeAI instance."""
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def get_nutrition_plan_chain():
    """
    Creates and returns a chain for generating a nutrition plan.
    """
    prompt_template = get_prompt_template("nutrition_plan_prompt.md")
    prompt = ChatPromptTemplate.from_template(prompt_template)
    llm = get_llm()
    return prompt | llm | StrOutputParser()

def get_shopping_list_chain():
    """
    Creates and returns a chain for generating a shopping list.
    """
    prompt_template = get_prompt_template("shopping_list_prompt.md")
    prompt = ChatPromptTemplate.from_template(prompt_template)
    llm = get_llm()
    return prompt | llm | StrOutputParser()

def get_exercise_routine_chain():
    """
    Creates and returns a chain for generating an exercise routine.
    """
    prompt_template = get_prompt_template("exercise_routine_prompt.md")
    prompt = ChatPromptTemplate.from_template(prompt_template)
    llm = get_llm()
    return prompt | llm | StrOutputParser()