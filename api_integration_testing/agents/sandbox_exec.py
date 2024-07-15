import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate

from langchain.agents import AgentExecutor, create_tool_calling_agent, tool
from langchain_community.tools import ShellTool
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.tools import Tool

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")

gpt_model = ChatOpenAI(model="gpt-4o",api_key=api_key)

shell_tool = ShellTool()

toolkit = FileManagementToolkit()
cpy_tool,del_tool,search_tool,move_file_tool,read_tool,write_tool,list_dir=toolkit.get_tools()
    
execution_tools = [shell_tool,cpy_tool,del_tool,search_tool,move_file_tool,read_tool,write_tool,list_dir]

test_code_gen_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
         You are an assistant who will execute the 

         Input - project root folder path

         Tasks - 
            - To start the execution, firstly navigate to root project path
            - then use the shell_tool to execute the following commands - 
                - 'mvn clean install'
                - 'mvn test'
            - if 'BUILD SUCCESS' then return True 
            - else return False along with summary of the error message containing necessary information only.  

        """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(gpt_model, execution_tools, test_code_gen_prompt)

sandbox_agent_executor = AgentExecutor(agent=agent, tools=execution_tools, verbose=True, stream_runnable=False)