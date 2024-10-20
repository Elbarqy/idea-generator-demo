import asyncio
import csv
from agents import IdeaGeneratorAgent, AgentAgainst, AgentFor, Evaluator
import re


def extract_percentages(text):
    pattern = r'\d+\%'
    percentages = re.findall(pattern, text)
    return percentages


def clean_up(text):
    return text.replace(",", ".").replace("\n", " ").replace("\"", "").replace("-", "")


def append_to_csv(file_path, data):
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(data)


async def generate(topic, generated):
    counter = 0
    for idea in generated[2:-1]:
        idea_comp = idea.split(',')
        if len(idea_comp) != 2:
            idea_comp = idea.split(";")
            if len(idea_comp) != 2:
                continue
        print("Generated Idea : " + idea)
        print("Calculating positive points......")
        positive = await AgentFor().generate_suggestions(idea)
        print("POSITIVE : " + positive.text)
        print("Calculating negative points......")
        negative = await AgentAgainst().generate_suggestions(idea)
        print("NEGATIVE : " + negative.text)
        print("EVALUATING......")
        evaluation = await Evaluator().generate_suggestions(idea=idea, pros=positive.text, cons=negative.text)
        print("evalutation: " + evaluation.text)
        find_eval = extract_percentages(evaluation.text)
        percentage = 0
        if (len(find_eval) != 0):
            percentage = find_eval[0]
        temp = [
            clean_up(idea.split(',')[0]),
            clean_up(idea.split(',')[1]),
            clean_up(positive.text),
            clean_up(negative.text),
            percentage
        ]
        append_to_csv(topic+".csv", temp)
        counter += 1
    return counter


async def main():
    topic = input("please enter your topic: ")
    number_of_ideas = input("How many ideas to generate: ")

    generator = IdeaGeneratorAgent()
    counter = 0
    append_to_csv(
        topic+".csv", "idea,description,positive,negative,evaluation".split(","))
    n = int(number_of_ideas)
    result = await generator.generate_suggestions(topic=topic, number=number_of_ideas)
    while counter < n:
        generated_ideas = result.text.split("\n")
        counter += await generate(topic=topic, generated=generated_ideas)
        if (counter < n):
            result = await generator.generate_more()

    # print(result)


if __name__ == "__main__":
    asyncio.run(main())
