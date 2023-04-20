from dotenv import load_dotenv
from lib.person import *
import os
import openai

load_dotenv()
openai.api_key: str = os.environ["OPENAI_API_KEY"]


def main() -> None:
    message: str = input("Fill in the prompt: ")
    answer: str = mama(prompt=message)

    print(answer)


main()ー
