#import utils
#from utils import get_api_key
import os
import google.generativeai as palm
from google.api_core import client_options as client_options_lib
from google.api_core import retry
import pprint

pp = pprint.PrettyPrinter(indent=4)

# Get the value of the "MY_ENV_VAR" environment variable
env_var = os.environ.get("PALM_API_KEY")

palm.configure(api_key=env_var)
#               transport="rest",
#               client_options=client_options_lib.ClientOptions(
#                api_endpoint=os.getenv("GOOGLE_API_BASE"),)

# for m in palm.list_models():
#     print(f"name: {m.name}")
#     print(f"description: {m.description}")
#     print(f"generation methods:{m.supported_generation_methods}\n")

models = [m for m in palm.list_models() 
          if "generateText" 
          in m.supported_generation_methods]
# print(models)

model_bison = models[0]
# pp.pprint(model_bison)

@retry.Retry()
def generate_text(prompt,
                  model=model_bison,
                  temperature=0.0):
    return palm.generate_text(prompt=prompt,
                              model=model,
                              temperature=temperature)

# example 1
prompt = "Show me how to iterate across a list in Python."

completion = generate_text(prompt)

print(completion.result)

# example 2
prompt = "write code to iterate across a list in Python"

completion = generate_text(prompt)

print(completion.result)

# example 3
prompt = "show me how to read an environment variable in Python"

completion = generate_text(prompt)

print(completion.result)