import os 
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv

load_dotenv()

model = 'deepseek-r1'
llm_config = {
    "model": model, 
    "api_key": os.environ.get("DS_KEY"), 
    "base_url": os.environ.get("BASE_URL"),
}

assistant = AssistantAgent(
    name = 'assistant', 
    system_message="You are responsible for code generation. Please communicate with user agent and fix any issues.", 
    llm_config=llm_config, 
)

user = UserProxyAgent(
    name = 'user', 
    system_message="You are responsible for code executor. Please communicate with assistant agent and fix any issues. Ask for user feedback at the end of code execution.", 
    human_input_mode="TERMINATE", 
    code_execution_config={
        "work_dir": "coding", 
        "use_docker": False,
    }, 
    llm_config=llm_config, 
)

user.initiate_chat(assistant, message="Plot META & APPLE stock for last 12 months.")