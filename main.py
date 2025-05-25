import chainlit as cl
from chainlit.types import ThreadDict
from chainlit.input_widget import Select, Switch, Slider

from llama_index.core.base.llms.types import MessageRole, ChatMessage
from llama_index.core.agent.workflow import FunctionAgent, AgentStream, ToolCall
from llama_index.core.workflow import Context
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.tools import FunctionTool

from llms import get_gemini_llm, LLMConfig
from history import CustomMemory
from logger import rich_logger
from tools import (
    calculate_sum, 
    calculate_average,
    calculate_sqrt
)


@cl.on_chat_start
async def start():
    """Handler for chat start events. Sets session variables."""

    try:
        await cl.Message(
            content="Welcome! I'm your AI assistant. How can I help you today?",
            author="Assistant"
        ).send()
        rich_logger.info("Welcome message sent")

        tools = [
            FunctionTool.from_defaults(
                fn=calculate_sum,
                name="calculate_sum",
                description="Adds two numbers together. For example: To add 5 and 3, use this function with x=5 and y=3"
            ),
            FunctionTool.from_defaults(
                fn=calculate_average,
                name="calculate_average",
                description="Calculates the average (arithmetic mean) of two numbers. For example: For numbers 4 and 6, use this function with x=4 and y=6"
            ),
            FunctionTool.from_defaults(
                fn=calculate_sqrt,
                name="calculate_sqrt",
                description="Calculates the square root of a non-negative number. For example: To find square root of 16, use this function with number=16"
            )
        ]

        gemini_llm = get_gemini_llm()
        agent = FunctionAgent(tools=tools, llm=gemini_llm)
        
        cl.user_session.set("agent", agent)
        cl.user_session.set("context", Context(agent))
        cl.user_session.set("agent_tools", tools)
        cl.user_session.set("llm", gemini_llm)
        cl.user_session.set("memory", CustomMemory())
        cl.user_session.set("greet", False)
        
        rich_logger.success("Session variables initialized successfully")

        settings = await cl.ChatSettings(
            [            
                Select(
                    id="LLM",
                    label="Gemini model to use",
                    values=["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"],
                    initial_index=0,
                ),
                Switch(
                    id="Greet_on_message",
                    label="Greet user when message is received",
                    initial=False,
                ),
                Slider(
                    id="Temperature",
                    label="Temperature of the LLM",
                    initial=0.0,
                    min=0.0,
                    max=1.0,
                    step=0.1
                )
            ]
        ).send()
        rich_logger.success("Chat settings initialized successfully")

    except Exception as e:
        rich_logger.error("Error during chat start", exc_info=e)
        await cl.Message(
            content="Sorry, there was an error starting the chat.",
            author="System"
        ).send()


@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming messages"""
    try:
        rich_logger.info(f"Received message: {message.content[:50]}...")
        
        greet = cl.user_session.get("greet", False)
        if greet:
            await cl.Message(content="Hello there!", author="Assistant").send()
            rich_logger.info("Greeting message sent")
        
        agent = cl.user_session.get("agent")
        custom_memory = cl.user_session.get("memory")
        history = await custom_memory.get_history()
        chat_history = [
            ChatMessage(role=MessageRole(msg["role"]), content=msg["content"])
            for msg in history
        ]
        context = cl.user_session.get("context")
        
        msg = cl.Message(content="", author="Assistant")
        
        handler = agent.run(message.content, chat_history=chat_history, ctx=context)
        
        async for event in handler.stream_events():
            if isinstance(event, AgentStream):
                await msg.stream_token(event.delta)
                rich_logger.debug(f"Streaming token: {event.delta}")
            elif isinstance(event, ToolCall):
                with cl.Step(name=f"{event.tool_name} tool", type="tool"):
                    rich_logger.info(f"Tool called: {event.tool_name}")
                    continue
        
        response = await handler
        rich_logger.success(f"Generated response successfully: {str(response)[:50]}...")
        
        await msg.send()
        
        await custom_memory.add_message(ChatMessage(role=MessageRole.USER, content=message.content))
        await custom_memory.add_message(ChatMessage(role=MessageRole.ASSISTANT, content=str(response)))
        rich_logger.info("Messages added to memory")
        
    except Exception as e:
        rich_logger.error("Error processing message", exc_info=e)
        await cl.Message(
            content=f"Sorry, I encountered an error: {str(e)}", 
            author="Assistant"
        ).send()


@cl.on_stop
async def on_stop():
    """Handle when user stops the conversation"""
    await cl.Message(content="You have stopped the task!", author="System").send()
    rich_logger.warning("User stopped the conversation")


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    """Handle chat resume from thread"""
    try:
        rich_logger.info(f"Resuming chat from thread: {thread.get('id', 'unknown')}")
        
        custom_memory = CustomMemory()
        
        if "steps" in thread:
            await custom_memory.load_from_thread(thread["steps"])
            rich_logger.info("Chat history loaded from thread")
        
        cl.user_session.set("memory", custom_memory)

        gemini_llm = get_gemini_llm()
        agent_tools = cl.user_session.get("agent_tools", [])
        agent = FunctionAgent(tools=agent_tools, llm=gemini_llm)
        
        cl.user_session.set("agent", agent)
        cl.user_session.set("context", Context(agent))
        cl.user_session.set("llm", gemini_llm)

        rich_logger.success("Chat resumed successfully")
        
    except Exception as e:
        rich_logger.error("Error resuming chat", exc_info=e)
        await cl.Message(
            content="Sorry, there was an error resuming the chat.",
            author="System"
        ).send()


@cl.on_chat_end
def on_chat_end():
    """Handle chat end"""
    rich_logger.info("A user has ended the chat")


@cl.on_settings_update
async def setup_agent(settings):
    """Handler to manage settings updates"""
    try:
        rich_logger.info(f"Updating settings: {settings}")
        
        gemini_llm = get_gemini_llm(
            config=LLMConfig(
                model=settings["LLM"],
                temperature=settings["Temperature"]
            )
        )
        
        agent_tools = cl.user_session.get("agent_tools", [])
        agent = FunctionAgent(tools=agent_tools, llm=gemini_llm)
        
        cl.user_session.set("agent", agent)
        cl.user_session.set("context", Context(agent))
        cl.user_session.set("greet", settings["Greet_on_message"])
        
        rich_logger.success("Settings updated successfully")
        
    except Exception as e:
        rich_logger.error("Error updating settings", exc_info=e)


@cl.on_mcp_connect
async def on_mcp_connect(connection):
    """Handler to connect to an MCP server. 
    Lists tools available on the server and connects these tools to
    the LLM agent."""
    
    openai_llm = cl.user_session.get("llm")
    mcp_cache = cl.user_session.get("mcp_tool_cache", {})
    mcp_tools = cl.user_session.get("mcp_tools", {})
    agent_tools = cl.user_session.get("agent_tools", [])
    try:
        rich_logger.info("Connecting to MCP")
        mcp_client = BasicMCPClient(connection.url)
        rich_logger.info("Connected to MCP")
        mcp_tool_spec = McpToolSpec(client=mcp_client)
        rich_logger.info("Unpacking tools")
        new_tools = await mcp_tool_spec.to_tool_list_async()
        for tool in new_tools:
            if tool.metadata.name not in mcp_tools:
                mcp_tools[tool.metadata.name] = tool
                mcp_cache[connection.name].append(tool.metadata.name)
        agent = FunctionAgent(
            tools=agent_tools + list(mcp_tools.values()),
            llm=openai_llm,
        )
        cl.user_session.set("agent", agent)
        cl.user_session.set("context", Context(agent))
        cl.user_session.set("mcp_tools", mcp_tools)
        cl.user_session.set("mcp_tool_cache", mcp_cache)
        await cl.Message(f"Connected to MCP server: {connection.name} on {connection.url}", type="assistant_message").send()

        await cl.Message(
            f"Found {len(new_tools)} tools from {connection.name} MCP server.", type="assistant_message"
        ).send()
    except Exception as e:
        await cl.Message(f"Error conecting to tools from MCP server: {str(e)}", type="assistant_message").send()


@cl.on_mcp_disconnect
async def on_mcp_disconnect(name: str):
    """Handler to handle disconnects from an MCP server.
    Updates tool list available for the LLM agent.
    """
    openai_llm = cl.user_session.get("llm")
    agent_tools = cl.user_session.get("agent_tools", [])
    mcp_tools = cl.user_session.get("mcp_tools", {})
    mcp_cache = cl.user_session.get("mcp_tool_cache", {})
    
    if name in mcp_cache:
        for tool_name in mcp_cache[name]:
            del mcp_tools[tool_name]
        del mcp_cache[name]

    if len(mcp_tools) > 0:
        agent = FunctionAgent(
            tools=agent_tools + list(mcp_tools.values()),
            llm=openai_llm,
        )
    else:
        agent = FunctionAgent(
            tools=agent_tools,
            llm=openai_llm,
        )
    cl.user_session.set("context", Context(agent))
    cl.user_session.set("mcp_tools", mcp_tools)
    cl.user_session.set("mcp_tool_cache", mcp_cache)
    cl.user_session.set("agent", agent)
    
    await cl.Message(f"Disconnected from MCP server: {name}", type="assistant_message").send()


if __name__ == "__main__":
    cl.run()