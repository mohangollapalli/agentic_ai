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

# 3. Manager agent (It's NOT Group chat Manager..)
manager = AssistantAgent(name="manager", 
               system_message="""You answer in a polite way taht the problem 
                    will be looked into and resolved as soon as possible and will
                    get back to the customer later through email. 
                    Reply "TERMINATE" when you have no further input.""", 
                llm_config=llm_config)

def escalate(sender): 
    content = sender.chat_messages 
    messages = content[next(iter(content))]
    message_contents = [message['content'] for message in messages]
    all_messages = " ".join(message_contents) 
    important_words = ['critical', 'important', 'asap', 'urgent']
    # trigger = true or false
    return any(word in all_messages.split() for word in important_words)

specialist.register_nested_chats(
    [
        {"recipient": manager, 
        "summary_method": "last_msg", 
        "message": "Treat this urgently and respond in a professional manner.",
        "max_turns": 1}
    ], 
    trigger=lambda sender: sender is user and escalate(sender)
)

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