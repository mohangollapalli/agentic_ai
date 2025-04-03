import os 
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv

load_dotenv()

model = 'gpt-4o'
llm_config = {
    "model": model, 
    "api_key": os.environ.get("OPENAI_KEY"), 
    "base_url": os.environ.get("BASE_URL"),
    "price": [0.0, 0.0], 
}

# user agent 
user = UserProxyAgent(name="user", 
                      human_input_mode="ALWAYS", 
                      code_execution_config=False, 
                      llm_config=llm_config)

# 1. specialist

specialist = AssistantAgent(name="specialist", 
               system_message="""You are an expert customer care representative of a bank. 
                    Your objective is to provide the user with the best possible banking solutions and service. 
                    Always greet the customer at the start.
                    If the user responds with 'exit' or 'TERMINATE', reply once with "HANDOVER_TO_SURVEYOR" and stop responding.""", 
                    llm_config=llm_config)
# 2. surveyor 
surveyor = AssistantAgent(name="surveyor", 
               system_message="""You are responsible for collecting customer satisfaction ratings. 
                    Ask the user to rate their service experience on a scale of 1 to 10.
                    If the user responds with 'exit' or 'TERMINATE', say "Thank you for your time!" and stop responding.""", 
                    llm_config=llm_config)

user.initiate_chats(
    [
        {"recipient": specialist, 
         "message": "Hello", 
         "summary_method": "reflection_with_llm"
        }, 
         {"recipient": surveyor, 
          "message": "Please ask the user to rate their service experience on a scale of 1 to 10.",
          "carryover": ["context", "summary"], 
          "trigger_condition": "HANDOVER_TO_SURVEYOR"
          }
    ]
)