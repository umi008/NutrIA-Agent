import asyncio
from langchain_core.runnables import RunnableParallel, RunnableLambda
from src.agent import create_agent
from src.chains import (
    get_nutrition_plan_chain,
    get_shopping_list_chain,
    get_exercise_routine_chain,
)

def parse_agent_output(agent_response):
    """
    Parses the agent's response to extract user data and tool outputs.
    """
    user_data_str = agent_response["output"]
    intermediate_steps = agent_response.get("intermediate_steps", [])

    # Extract data from the conversational output
    lines = user_data_str.split('\n')
    user_data_dict = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            user_data_dict[key.strip()] = value.strip()

    # Extract tool outputs
    tool_outputs = {
        "imc": next((step[1] for step in intermediate_steps if step[0].tool == 'calculate_bmi'), None),
        "tmb": next((step[1] for step in intermediate_steps if step[0].tool == 'calculate_bmr'), None),
        "macros": next((step[1] for step in intermediate_steps if step[0].tool == 'calculate_macros'), None),
    }

    # Combine all data into a single dictionary
    final_data = {
        "datos_usuario": user_data_str,
        "likes": user_data_dict.get("Comidas favoritas", ""),
        "dislikes": user_data_dict.get("Alimentos que no te gustan", ""),
        "objetivo_usuario": user_data_dict.get("Objetivo principal", ""),
        "nivel_experiencia": user_data_dict.get("Nivel de Actividad Física", ""),
        "preferencias_ejercicio": user_data_dict.get("Tipo de rutina preferida", ""),
        "dias_entrenamiento": user_data_dict.get("Frecuencia de entrenamiento", ""),
        "equipamiento_disponible": user_data_dict.get("Lugar de entrenamiento", ""),
        **tool_outputs
    }
    return final_data

async def main():
    """
    Main execution script for the wellness agent.
    """
    # Create the agent
    agent_executor = create_agent()
    chat_history = []

    # Welcome message
    print("Welcome to the Wellness Agent!")
    
    # Initial prompt
    initial_input = input("Please describe your wellness goals: ")
    chat_history.append({"role": "user", "content": initial_input})

    while True:
        # Invoke the agent with the current conversation history
        agent_response = await agent_executor.ainvoke({
            "input": initial_input,
            "chat_history": chat_history
        })
        
        # Print the agent's response
        print(f"\nAgent: {agent_response['output']}")
        chat_history.append({"role": "assistant", "content": agent_response["output"]})

        # Check if all necessary calculation tools have been called
        intermediate_steps = agent_response.get("intermediate_steps", [])
        called_tools = {step[0].tool for step in intermediate_steps}
        
        if 'calculate_bmi' in called_tools and \
           'calculate_bmr' in called_tools and \
           'calculate_macros' in called_tools:
            print("\nAll necessary data collected. Generating your wellness plan...")
            parsed_data = parse_agent_output(agent_response)
            break
        
        # Get the next input from the user
        user_input = input("Your response: ")
        chat_history.append({"role": "user", "content": user_input})
        initial_input = user_input # The next input to the agent is the latest user message

    # Define the parallel execution of chains
    map_chain = RunnableParallel(
        nutrition_plan=get_nutrition_plan_chain(),
        exercise_routine=get_exercise_routine_chain(),
    )

    # Add the shopping list chain
    full_chain = map_chain | RunnableParallel(
        shopping_list=RunnableLambda(
            lambda x: get_shopping_list_chain().invoke({"plan_nutricional": x["nutrition_plan"]})
        ),
        nutrition_plan=lambda x: x["nutrition_plan"],
        exercise_routine=lambda x: x["exercise_routine"],
    )

    # Invoke the parallel chain with user data
    results = await full_chain.ainvoke(parsed_data)

    # Print the results
    print("\n--- Your Personal Wellness Plan ---")
    print("\n### Nutrition Plan ###")
    print(results["nutrition_plan"])
    print("\n### Shopping List ###")
    print(results["shopping_list"])
    print("\n### Exercise Routine ###")
    print(results["exercise_routine"])
    print("\n---------------------------------")

if __name__ == "__main__":
    asyncio.run(main())