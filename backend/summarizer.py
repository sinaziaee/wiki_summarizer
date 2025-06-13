# from dotenv import load_dotenv
# import os
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
# import warnings
# warnings.filterwarnings('ignore')

# def load_chat_model_and_template():
#     template_string = """You are a helpful assistant.
#     Summarize the following Wikipedia article **clearly and concisely** in ≤{max_words} words.
#     ARTICLE:
#     \"\"\"
#     {article}
#     \"\"\"
#     """
#     prompt_template = ChatPromptTemplate.from_template(template_string)
#     load_dotenv()
#     chat = ChatOpenAI(
#         model="gpt-4o-mini",
#         temperature=0,
#         openai_api_key=os.environ['OPENAI_API_KEY'],
#     )
#     return chat, prompt_template

# def summarize(chat: ChatOpenAI, prompt_template: ChatPromptTemplate.from_template, text: str, max_words: int = 300):
#     article_text = prompt_template.format_messages(
#                     max_words=max_words,
#                     article=text)
#     summarized_article = chat(article_text)
#     return summarized_article.content

from __future__ import annotations   # for forward-refs in type hints
import os, textwrap, tiktoken, time
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from openai import OpenAIError

MAX_WORDS = 300                    # project spec
MODEL     = "gpt-4o-mini"

def _truncate(article: str, max_tokens: int = 6_000) -> str:
    """Hard-limit article length so we never exceed context."""
    enc = tiktoken.encoding_for_model(MODEL)
    tokens = enc.encode(article)
    if len(tokens) <= max_tokens:
        return article
    return enc.decode(tokens[:max_tokens])

def load_chat_model_and_template() -> tuple[ChatOpenAI, ChatPromptTemplate]:
    template = (
        "You are a helpful assistant.\n"
        "Summarize the following Wikipedia article **clearly and concisely** "
        f"in ≤{MAX_WORDS} words.\n\n"
        "ARTICLE:\n\"\"\"\n{article}\n\"\"\""
    )
    prompt = ChatPromptTemplate.from_template(template)

    load_dotenv()
    chat = ChatOpenAI(
        model=MODEL,
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        request_timeout=60,
    )
    return chat, prompt

def summarize(
    chat: ChatOpenAI,
    prompt_template: ChatPromptTemplate,
    text: str,
    max_words: int = MAX_WORDS,
    retries: int = 3,
) -> str:
    """Return a ≤ max_words summary or raise on failure."""
    text = _truncate(text)               # protect context window

    messages = prompt_template.format_messages(article=text)
    backoff = 1
    for attempt in range(retries):
        try:
            response = chat(messages)
            summary = " ".join(response.content.split())     # squash whitespace
            if len(summary.split()) > max_words:
                summary = " ".join(summary.split()[:max_words]) + " …"
            return textwrap.fill(summary, width=100)
        except OpenAIError as e:
            if attempt == retries - 1:
                raise
            time.sleep(backoff)
            backoff *= 2                # simple exponential back-off
