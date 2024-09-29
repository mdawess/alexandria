import ollama
import pandas as pd
import io
import sys

data = {
    'Name': ['John', 'Mary', 'Jane', 'Bob'],
    'Age': [25, 31, 22, 40],
    'Gender': ['Male', 'Female', 'Female', 'Male'],
    'City': ['New York', 'San Francisco', 'Chicago', 'Boston']
}

# Convert the dictionary into a DataFrame
df = pd.DataFrame(data)

prompt = f"""
You are a data analyst who uses python to analyze and provide insights on data.
Please assume the pandas dataframe will always have the name 'df' and write all
code in python. If a query is asked about the data, please return the necessary
python code to get the result.
Always return code in the format: ```python\n <code> ```

Please use this data for all analysis: {df.head()}

Note: Assume all queries relate to the provided dataset
"""

setup_prompt = ollama.generate(model='llama3.1', prompt=prompt)

while True:
    user_prompt = input("> ")
    if user_prompt == "exit" or user_prompt == "quit":
        break

    updated_prompt = prompt + "\n" + user_prompt
    resp = ollama.generate(model='llama3.1', prompt=updated_prompt)

    # Check if python code is included
    response = resp['response']
    code_start = response.find("```python")
    if code_start != -1:
        # Get the python code
        code = response.split('```python\n')[1].split('```')[0].strip()

        # print(f"Code to be executed: {code}")
        
        # Capture the output of the executed code
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()

        exec(code)

        sys.stdout = old_stdout
        ans = redirected_output.getvalue()

        # print(f"Execution result: {ans}")

        ans_template = f"""
        Here is the original user query: {user_prompt}

        Here is the answer that was returned: {ans}

        Can you please format this into a concise answer?
        """

        # print(f"Answer template: {ans_template}")

        insight = ollama.generate(model='llama3.1', prompt=ans_template)
        print(insight['response'])

    else:
        print(response)
