import os
import re
from typing import Literal

from openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain.output_parsers.fix import OutputFixingParser
from langchain_core.pydantic_v1 import BaseModel, Field

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("openai-api-key"))

system_prompt = """You are a data scientist working for an e-commerce company. Following tables are available to you:
Sales (date, revenue): 
This table contains revenue earned at each month. 

Costs (datetime, category, amount)
This table contains costs at each month divided by different categories (such as, utilities, logistics, ...). This table does not include costs due to tax. 

Tax (datetime, amount, is_paid)
This table contains amount of tax at each month. The column is_paid shows whether this amount is paid or not. 

You have already created data using following sql queries:
1. select year(datetime), month(datetime), sum(revenue) from Sales group by year(datetime), month(datetime);
2. select sum(amount) from Costs group by category;
"""

# A C-Level manager at this e-commerce company has the following questions: {question}

# {options}"""


def invoke_feasibility_chain(question: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"A C-Level manager at this e-commerce company has the following questions: {question}",
            },
            {
                "role": "assistant",
                "content": """You have the following options to choose from:
                            * It is feasible, we can use one of the sql queries mentioned above to answer the question.  
                            * It is partially feasible, given the data we can build a new sql query that answers the question.
                            * It is not feasible, given the data available it is not possible to answer this question
                            
                            Prioritize using sql queries that you have already created. 
                            You can expect the user to do simple calculations by hand. For instance, if you are showing top 10 highest costs, you can expect the user to identify the top 3.
                            Or, if you are showing the revenue over time, you can expect the user to identify the maximum or minimum values.

                            Think step by step.
                            
                            Output one of these three words: 
                            - feasible 
                            - partially feasible 
                            - not feasible""",
            },
        ],
        temperature=0,
    )

    try:
        is_feasible = response.choices[0].message.content

        if is_feasible in ["feasible", "partially feasible", "not feasible"]:
            return is_feasible
        else:
            raise ValueError(
                f'Response {is_feasible} is not among acceptable values: "feasible", "partially feasible", "not feasible"'
            )
    except:
        raise ValueError("invalid response")


def invoke_graph_selection_chain(question: str):

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"A C-Level manager at this e-commerce company has the following questions: {question}",
            },
            {
                "role": "assistant",
                "content": """Think step by step. First identify the sql query that is needed to answer the question. Then check which one of the available sql queries can be used. 
                            You have the following options to choose from:
                            * sql query 1
                            * sql query 2
                            
                            Output one of these two numbers: 
                            - 1 
                            - 2""",
            },
        ],
        temperature=0,
    )

    try:
        graph_id = response.choices[0].message.content
        graph_id = int(graph_id)

        if graph_id in [1, 2]:
            return graph_id
        else:
            raise ValueError(
                f"Response {graph_id} is not among acceptable values: 1, 2"
            )
    except:
        raise ValueError("invalid response")


def invoke_sql_query_chain(question):

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"A C-Level manager at this e-commerce company has the following questions: {question}",
            },
            {
                "role": "assistant",
                "content": """Think step by step. Consider the available tables. Make a sql query that answers the question. 
                            Output a runnable sql query. Only output the code block. Do not output any explanation.""",
            },
        ],
        temperature=0,
    )

    try:
        sql_query = response.choices[0].message.content

        sql_query = sql_query.replace("```", "").replace("sql", "")

        import sqlparse

        def check_sql_query(query):
            try:
                parsed = sqlparse.parse(query)
                if not parsed:
                    raise ValueError("The query is empty or invalid.")
                for statement in parsed:
                    if not statement.is_group:
                        raise ValueError("The query is not a valid SQL statement.")
                return True
            except:
                return False

        is_valid_query = check_sql_query(sql_query)
        if is_valid_query:
            return sql_query
        else:
            raise Exception(f"The following SQL query is not valid: {sql_query}")

    except:
        raise ValueError("invalid response")
