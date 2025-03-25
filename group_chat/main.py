import os 
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv

load_dotenv()

model = 'gpt-4o-mini'
llm_config = {
    "model": model, 
    "api_key": os.environ.get("OPNAI_MINI_KEY"),
    "base_url": os.environ.get("BASE_URL"), 
    "temperature":0, 
    "price": [0.0, 0.0], 
}

user = UserProxyAgent(name="user", 
               human_input_mode="TERMINATE", 
               code_execution_config={
                   "work_dir":"sudoku_game", 
                   "use_docker": False, 
               }, 
               llm_config=llm_config)

# 1. Sudoku Generator 
sudoku_gen = AssistantAgent(name="sudoku_generator", 
                            system_message="You are responsible for generating a valid 9x9 sudoku puzzle based on the difficulty level provided by the user : Easy, Medium or Hard. After generating the puzzle explicitly call sudoku_solver.", 
                            llm_config=llm_config)

# 2. Sudoku Solver
sudoku_solver = AssistantAgent(name="sudoku_solver", 
                            system_message="You are responsible for providing a solution to the given 9x9 sudoku puzzle. After generating the solution explicitly call sudoku_verifier.", 
                            llm_config=llm_config)

# 3. Sudoku Verifier
sudoku_verifier = AssistantAgent(name="sudoku_verifier", 
                            system_message="You are responsible for verifying the given sudoku solution for 9x9 sudoku puzzle. Please consider all 9x9 sudoku puzzle rules while verifying. After verifying explicitly call sudoku_visualizer.", 
                            llm_config=llm_config)

# 4. Sudoku Viz
sudoku_viz = AssistantAgent(name="sudoku_visualizer", 
                            system_message="You create a visually appealing Sudoku representation for display.", 
                            llm_config=llm_config)

groupchat = GroupChat(agents=[user, sudoku_gen, sudoku_solver, sudoku_verifier, sudoku_viz], 
                      messages=[])
groupchat_mgr = GroupChatManager(groupchat, 
                 llm_config=llm_config)

def play_sudoku(difficulty='easy'):
    user.initiate_chat(groupchat_mgr, 
                    message={
                        "role": "user",
                        "content": f"Generate a {difficulty} Sudoku Puzzle and solution."
                    })

play_sudoku('easy')