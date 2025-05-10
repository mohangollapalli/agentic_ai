import os 
import sqlite3
import pandas as pd
from autogen import AssistantAgent, UserProxyAgent, register_function, GroupChat, GroupChatManager
from dotenv import load_dotenv

shared_state = {}
DB_FILE = "/Users/mohan/agents/group_chat/shared_state.db"

load_dotenv()

model = 'gpt-4.1'
llm_config = {
    "model": model, 
    "api_key": os.environ.get("OPENAI_41_KEY"),
    "base_url": os.environ.get("BASE_URL"), 
    "temperature":0, 
    "price": [0.0, 0.0], 
    "timeout": 120,
}

def load_data(file_name: str) -> pd.DataFrame:
    file_path = f"/Users/mohan/agents/group_chat/{file_name}"
    data = pd.read_csv(file_path)
    with sqlite3.connect(DB_FILE) as conn: 
        data.to_sql("imdb_data", conn, if_exists="replace", index=False)
    return data

user = UserProxyAgent(
    name="user", 
    system_message="""
        Please communicate with data assistant to load the dataset using load_data(file_name) function.
        ALWAYS load data from shared_state. If shared_state["imdb_data"] is None or empty, respond with a message: "Data not loaded yet. Please ask data_assistant to load the dataset."
        TERMINATE upon completion.""", 
    code_execution_config=False, 
    human_input_mode="TERMINATE", 
    llm_config=llm_config
)

data_assistant = AssistantAgent(
    name="data_assistant", 
    system_message="""
        You are responsible for loading the dataset using load_data function or tool that is registered.
        DO NOT generate code for load_function. Use the load_data function that is registered for execution.
        After loading the data and saving it to shared_state, HAND OFF the conversation to the user agent.
        DO NOT TERMINATE the conversation after loading data.""", 
    code_execution_config={"use_docker":False, 
                           "work_dir":"./code"}, 
    llm_config=llm_config
)
register_function(
    load_data, 
    caller=user, 
    executor=data_assistant, 
    name="load_data", 
    description="This function load_data(file_name) loads the imdb movie dataset and writes the result into shared_state.db."
)

user.initiate_chat(
    data_assistant, 
    message={
        "role": "user", 
        "content": """
        This is a two steps process. Execute the below steps in order.
            1. First, data_assistant should load the dataset with file_name="imdb_dataset.csv" using the load_data(file_name) function. Load the data to shared_state db and table "imdb_data".
            2. Second, return and print the data.
        Please ensure all these steps are completed in sequence. Once the result is obtained please TERMINATE."""
    }, max_turns=20
)
