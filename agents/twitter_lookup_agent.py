from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType

from tools.tools import get_twitter_username


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model="gpt-4")
    template = """given the full name {name_of_person} I want you to get it me a username of their Twitter acount.
                        Your answer should contain only a username, without '@' symbol. """
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 twitter account",
            func=get_twitter_username,
            description="useful for when you need get the Twitter Page URL",
        )
    ]
    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    promt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    twitter_user_name = agent.run(promt_template.format(name_of_person=name))
    return twitter_user_name
