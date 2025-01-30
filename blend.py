import pandas as pd
import re
from openai import OpenAI
import blendsql
from blendsql.ingredients import LLMMap, LLMQA, LLMJoin
from blendsql.db import Pandas
from blendsql.models import OpenaiLLM
from LLM import call_gemini, call_openai

# Optionally set how many async calls to allow concurrently
# This depends on your OpenAI/Anthropic/etc. rate limits
blendsql.config.set_async_limit(10)

# Load model
model = OpenaiLLM("gpt-4o-mini") # requires .env file with `OPENAI_API_KEY`

def openai_llm(prompt):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a data scientist."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.5,
        top_p=1.0,
        n=1,
        stop=None
    )
    return response.choices[0].message.content.strip()

def evaluate(final_table, question, table_name):
        # Create the prompt for the first API call
        prompt = f"""
        Table: {table_name}
        {final_table.to_string(index=False)}

        Question: {question}
        
        Answer the question given the table in as short as possible.
        If the table has just one column and value consider that as the answer given the column name.
        Just provide the answer, do not provide any other information.
        """    
        return openai_llm(prompt)

# Function to generate BlendSQL query using OpenAI
def generate_blendsql_query(table, question):
    prompt = f"""
    Generate BlendSQL given the question, table, passages, image captions to answer the question correctly.
    BlendSQL is a superset of SQLite, which adds external function calls for information not found within native SQLite.
    These external functions should be wrapped in double curly brackets.

    If question-relevant column(s) contents are not suitable for SQL comparisons or calculations, map it to a new column with clean content by a new grammar:
        `LLMMap('question', '{{table}}::{{column}}')`

    If the questions comment on some relative datetime operation, use the new grammar:
        `DT('{{table}}::{{column}}', start='', end='')`

    
    """
    with open('blendPrompt', 'r') as file:
        blendPrompt = file.read()
    prompt += "\n\n" + blendPrompt

    prompt += f"""
      Columns: {table.columns}
      Table: {table.to_html()}
      Question: {question}
    """
    
    return openai_llm(prompt)

    # query = """
    #     SELECT * FROM w
    #     WHERE city = {{
    #         LLMQA(
    #             'Which city is located 120 miles west of Sydney?',
    #             (SELECT * FROM documents WHERE content LIKE '%sydney%'),
    #             options='w::city'
    #         )
    #     }}
    #     """

    # response = openai.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a data scientist."},
    #         {"role": "user", "content": prompt}
    #     ],
    #     max_tokens=150
    # )
    # return response.choices[0].message['content'].strip()

# Function to execute BlendSQL query and return the final answer

def extract_and_format_sql_query(message_content):
    if message_content.startswith("BlendSQL:"):
        message_content = message_content[len("BlendSQL:"):].strip()
    
    match = re.search(r"```sql\n(.*?)\n```", message_content, re.DOTALL)
    if match:
        query = match.group(1).strip()
        return query
    return message_content


def execute_blend(table, question, table_name, table_id):
    db = Pandas(
        {
            "w": table,
        }
    )


    # Get BlendSQL prompt from OpenAI
    query = generate_blendsql_query(table, question)
    # print(query)
    formatted_query = extract_and_format_sql_query(query)
    print(formatted_query)
    

    # # Execute BlendSQL query
    # smoothie = blendsql.blend(
    #     query=formatted_query,
    #     db=db,
    #     ingredients={LLMMap, LLMQA, LLMJoin},
    #     default_model=model,
    #     infer_gen_constraints=True,
    #     verbose=True
    # )
    try:
        # Execute BlendSQL query
        smoothie = blendsql.blend(
            query=formatted_query,
            db=db,
            ingredients={LLMMap, LLMQA, LLMJoin},
            default_model=model,
            infer_gen_constraints=True,
            table_to_title = {"w": table_name},
            verbose=True
        )
        # print(smoothie.meta.prompts)
        print(print('-'*30))
        print(table_id)
        print(print('-'*30))
        print(smoothie.df)
        result = evaluate(smoothie.df, question, table_name)
        return result, formatted_query, ""
    except Exception as e:
        error_message = str(e)
        print(f"An error occurred: {error_message}")
        # Return default values in case of failure
        return "error occured while trying to execute blend query", formatted_query, error_message

