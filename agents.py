from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
llmModel = "phi3.5"
responseMaxWords = 50


class IdeaGeneratorAgent:
    def __init__(self):
        self.llm = ChatOllama(
            model=llmModel,
            temperature=0.7,
            # callbacks=[StreamingStdOutCallbackHandler]
        )
        self.max_words = 8
        self.prompt_template = PromptTemplate(
            input_variables=["topic", "number"],
            template="As a creative entreprenure generate a list of {number} ideas in csv format about {topic} \n" +
            "keep each idea short, your output should look like \"idea\", \"description\"")

    async def generate_suggestions(self, topic, number):
        prompt = self.prompt_template.format(
            topic=topic, number=number)
        messages = [HumanMessage(content=prompt)]
        response = await self.llm.agenerate(messages=[messages])
        return response.generations[0][0]
    async def generate_more(self):
        prompt = PromptTemplate("generate More").format()
        messages = [HumanMessage(content=prompt)]
        response = await self.llm.agenerate(messages=[messages])
        return response.generations[0][0]


class AgentFor:
    def __init__(self):
        self.llm = ChatOllama(
            model=llmModel,
            temperature=0.7,
            # callbacks=[StreamingStdOutCallbackHandler]
        )
        self.max_words = responseMaxWords
        self.prompt_template = PromptTemplate(
            input_variables=["idea"],
            template="As an agent supporting this idea: {idea}\n" +
            "your response should be in bullet points only listing 2 reasons why this idea is the best idea the company should go for, be persuasive \n" +
            "make sure your bullet points are brief, no fillers, no more than {max_words} words"
        )

    async def generate_suggestions(self, idea):
        prompt = self.prompt_template.format(
            idea=idea, max_words=self.max_words)
        messages = [HumanMessage(content=prompt)]
        response = await self.llm.agenerate(messages=[messages])
        return response.generations[0][0]


class AgentAgainst:
    def __init__(self):
        self.llm = ChatOllama(
            model=llmModel,
            temperature=0.7,
            # callbacks=[StreamingStdOutCallbackHandler]
        )
        self.max_words = responseMaxWords
        self.prompt_template = PromptTemplate(
            input_variables=["idea"],
            template="As an agent Against this idea: {idea}\n" +
            "your response should be in bullet points only listing 2 reasons why this idea is bad for the company, list your reasons, be persuasive \n" +
            "make sure your bullet points are brief, no fillers, no more than {max_words} words"
        )

    async def generate_suggestions(self, idea):
        prompt = self.prompt_template.format(
            idea=idea, max_words=self.max_words)
        messages = [HumanMessage(content=prompt)]
        response = await self.llm.agenerate(messages=[messages])
        return response.generations[0][0]


class Evaluator:
    def __init__(self):
        self.llm = ChatOllama(
            model=llmModel,
            temperature=0.7,
            # callbacks=[StreamingStdOutCallbackHandler]
        )
        self.max_words = 1
        self.prompt_template = PromptTemplate(
            input_variables=["idea", "details"],
            template="forget you are an ai and keep your answer short, only display a score from 0% to 100% to show how good this idea is, {idea}\n"
            + "with pros: {pros}, and cons:- {cons}")

    async def generate_suggestions(self, idea, pros, cons):
        prompt = self.prompt_template.format(
            idea=idea, pros=pros, cons=cons, max_words=self.max_words)
        messages = [HumanMessage(content=prompt)]
        response = await self.llm.agenerate(messages=[messages])
        return response.generations[0][0]
