from typing import Tuple
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from third_parties.linkedin import scrape_linkeding_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent

from third_parties.twitter import scrape_user_tweets
from output_parsers import person_intel_parser, PersonIntel


def ice_break(name: str) -> Tuple[PersonIntel, str]:
    linkedin_profie_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkeding_profile(linkedin_profile_url=linkedin_profie_url)

    twitter_username = twitter_lookup_agent(name=name)
    print(twitter_username)

    tweets = scrape_user_tweets(username=twitter_username, num_tweets=100)

    summary_template = """
        given the Linkedin information {information} and twitter {twitter_information} about person from I wnat you to create:
        1. a short summary
        2. two interesting facts about them
        3. A topic that may interest them
        4. 2 creative Ice breakers to open a conversation with them
        \n{format_instructions}
    """
    summary_promt_template = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=1, model="gpt-4")

    chain = LLMChain(llm=llm, prompt=summary_promt_template)

    result = chain.run(linkedin_information=linkedin_data, twitter_information=tweets)
    print(result)
    return person_intel_parser.parse(result), linkedin_data.get("profile_pic_url")


name = "Elon Musk"

if __name__ == "__main__":
    print("Hello Langchain")
    ice_break(name=name)
