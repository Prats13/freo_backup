import os
import shutil
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, create_tool_calling_agent, tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from langchain_community.tools import ShellTool
from langchain_community.agent_toolkits import FileManagementToolkit
# from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_community.callbacks import get_openai_callback
from langchain_core.tools import Tool

from api_test_generation import test_code_agent_executor
from utils.create_sandbox import sandbox
from utils.project_structure import folder_structure
from sandbox_exec import sandbox_agent_executor

load_dotenv()

# In-built tools
api_key=os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4o",api_key=api_key)

shell_tool = ShellTool()

toolkit = FileManagementToolkit()
cpy_tool,del_tool,search_tool,move_file_tool,read_tool,write_tool,list_dir=toolkit.get_tools()

# Custom tools
@tool
def generate_test_code(collection_data,instrucions,root_project_path,fs=folder_structure):
    """
    Invokes an agent to generate the test code/codes for API testing 

    Args:
        collection_data : Postman Collection data
        fs: Folder structure for reference
        root_project_path: Root project path
        instructions: Instructions on generating the test codes

    Returns:
        test codes : Test codes for API testing 
    """
    test_code_result=test_code_agent_executor.invoke(
        {
            "input": f"""
                Postman Collection Data : {collection_data}

                Folder structure: {fs}

                Root project path: {root_project_path}

                Instructions for test code generation: {instrucions}
                """
        }
    )

    return test_code_result

@tool
def execute_test_code(project_root_path):
    """
    Executes the maven project created for api testing

    Returns:
        boolean: True if successfull execution or else False
        string: Details of error on unsuccessful execution
    """
    execute_code_result=sandbox_agent_executor.invoke(
        {
            "input": f"""
                Project root path = {project_root_path}
                """
        }
    )
    
    return execute_code_result

@tool
def create_sandbox_env():
    """
    Creates the sandbox environment for test code execution

    Returns:
        boolean: True if the sandbox is created successfully.
        string: Path to the sandbox environment
    """
    success, root_path = sandbox()

    return success,root_path

tools = [create_sandbox_env,generate_test_code,execute_test_code,shell_tool,cpy_tool,del_tool,search_tool,move_file_tool,read_tool,write_tool,list_dir]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
        You are an assistant who will coordinate a complete api integration testing procedure.

        Input - Postman collection of API endpoints json data.
        
        Tasks -
         - Read & process the input postman collection data.
         - Generate relevant test cases for each api endpoints.
         - Use 'generate_test_code' tool for test code generation to test the APIs.
            - Provide summarised instructions as one of the argument to the tool.  
         - Use 'execute_test_code' tool to execute the generated test code/codes.
         - If the execution is successfull then return a detailed test report containing all the relevant information.
         - If the execution fails then follow the following error handling steps - 
            Error Handling - 
             - Diagnose & resolve the error and retry execution of the test code/codes.
             - Repeat the error handling cycle untill all the errors are either resolved or not possible to solve.
             - Incase the error is irresolvable then return a summary of the error and recommend steps to resolve it.

        Important pointers for the tasks - 
         - If you are stuck in an error that corresponds to a particular API then move on to the next API and record the previous failures.
         - In the error handling cycle if you diagnose the problem is in the test code/codes then -
            - Create clear instructions for new test code generation and pass it to the 'generate_test_code' tool.
            - continue the cycle.

        Output format - Detaield Test Report.
        """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

input_data="""
Pass the input data here.
"""
agent = create_tool_calling_agent(model, tools, prompt)
goal_agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, stream_runnable=False)

with get_openai_callback() as total_token_cb:
    result = goal_agent_executor.invoke(
        {
        "input": f"""
        Postman Collection data - {input_data}
        """
        }
    )
