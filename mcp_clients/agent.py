import os
import asyncio
from langchain.chat_models import init_chat_model
# from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_mcp_adapters.client import MultiServerMCPClient
# from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

model_version = os.getenv("MODEL_VERSION", "claude-3-7-sonnet-latest")
model_provider = os.getenv("MODEL_PROVIDER", "anthropic")
mcp_server_path_serper = os.getenv("MCP_SERVER_PATH_SERPER")
word_count = 100

mcp_client = MultiServerMCPClient(
    {
        "news": {
            "command": "python3",
            # The full absolute path to MCP server .py file
            "args": [mcp_server_path_serper],
            "transport": "stdio",
        }
    }
)

model = init_chat_model(model_version, model_provider=model_provider)
# memory = InMemorySaver()

async def answer_topic(topic: str):
    tools = await mcp_client.get_tools()
    # TODO: agent = create_react_agent(model, tools, checkpointer=memory)
    agent = create_react_agent(model, tools)

    # REF: This code snippet doesn't work but is left here for reference
    # prompt_template = ChatPromptTemplate.from_messages([
    #     SystemMessage(content="You are an assistant to provide explanation or description of a certain topic. You will fetch additional information of this topic when needed."),
    #     HumanMessage(content="Tell me about {topic} in no more than {word_count} words, then include a summary of the recent news of {topic} in one separate paragraph.")
    # ])

    # Prompt template with constraints to prevent out-of-context information
    prompt_template = ChatPromptTemplate.from_messages([
        ("system",
         "You are an assistant to provide explanation or description of a certain topic. You will fetch additional information of this topic when needed."),
        ("user", """
Tell me about {topic} in no more than {word_count} words, then include a summary of the recent news of {topic} in one separate paragraph.
Write the news summary based STRICTLY on the news you found. DO NOT use any knowledge outside of the news you found.
If you found no news, respond with: There is no news about {topic}.
        """)
    ])

    prompt = prompt_template.invoke({"topic": topic, "word_count": f"{word_count}"})
    response = await agent.ainvoke(prompt)

    return response


if __name__ == '__main__':
    result = asyncio.run(answer_topic("Anthropic"))

    for message in result["messages"]:
        message.pretty_print()
