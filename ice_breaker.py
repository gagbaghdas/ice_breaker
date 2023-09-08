from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from third_parties.linkedin import scrape_linkeding_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

if __name__ == "__main__":
    print("Hello Langchain")

linkedin_profie_url = linkedin_lookup_agent(name="Gagik Baghdasaryan Frismos")

summary_template = """
    given the Linkedin information {information} about person from I wnat you to create:
    1. a short summary
    2. two interesting facts about them
"""
summary_promt_template = PromptTemplate(
    input_variables=["information"], template=summary_template
)

llm = ChatOpenAI(temperature=0, model="gpt-4")

chain = LLMChain(llm=llm, prompt=summary_promt_template)


linkedin_data = scrape_linkeding_profile(linkedin_profile_url=linkedin_profie_url)

print(chain.run(information=linkedin_data))
