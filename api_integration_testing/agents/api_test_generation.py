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

test_code_tools = [shell_tool,cpy_tool,del_tool,search_tool,move_file_tool,read_tool,write_tool,list_dir]

test_code_gen_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
         You are an assistant who will generate test code for API testing based on the postman collection and the folder structure

         Input - postman collection, root project path and project folder structure

         Tasks - 
            - Your initial task will be to analyse the postman collection then the folder structure which is a replica of a maven project
            - Then based on the information, generate and write code for the following - 
                - ConfigManager.java, ApiUtils.java, ResponseValidator.java, BaseTest.java
                - the test codes for each api in 'src/test/java/com/example/api/tests'
            - Finally return a boolean value based on successful code generation

        """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(gpt_model, test_code_tools, test_code_gen_prompt)

test_code_agent_executor = AgentExecutor(agent=agent, tools=test_code_tools, verbose=True, stream_runnable=False)