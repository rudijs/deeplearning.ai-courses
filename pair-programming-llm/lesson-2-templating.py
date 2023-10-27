import os

import google.generativeai as palm
from google.api_core import client_options as client_options_lib
from google.api_core import retry

import pprint
pp = pprint.PrettyPrinter(indent=4)

# Get the value of the "MY_ENV_VAR" environment variable
env_var = os.environ.get("PALM_API_KEY")

palm.configure(api_key=env_var)
# transport="rest",
# client_options=client_options_lib.ClientOptions(
# api_endpoint=os.getenv("GOOGLE_API_BASE"),
# )
# )

models = [m for m in palm.list_models()
          if "generateText"
          in m.supported_generation_methods]

model_bison = models[0]
# pp.pprint(model_bison)


@retry.Retry()
def generate_text(prompt,
                  model=model_bison,
                  temperature=0.0):
    return palm.generate_text(prompt=prompt,
                              model=model,
                              temperature=temperature)


prompt_template = """
{priming}

{question}

{decorator}

Your solution:
"""

priming_text = "You are an expert at writing clear, concise, Python code."
# priming_text = "You are an expert at writing clear, concise, Typescript code."

# question = "create a doubly linked list"
question = """create a very large list of random numbers in python, and then write code to sort that list"""

# option 1
# decorator = "Work through it step by step, and show your work. One step per line."

# option 2
decorator = "Insert comments for each line of code."

prompt = prompt_template.format(priming=priming_text,
                                question=question,
                                decorator=decorator)

# print(prompt)

completion = generate_text(prompt)

print(completion.result)
