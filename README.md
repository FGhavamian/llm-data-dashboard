# Streamlite dashboard powered by LLM

A pain point of using data dashboards is to find the graph you are looking for easily. Specifically: 
- the graph is hidden in between many others and it isn't easy to find it
- the graph you are looking for does not exist in the dashboard but, it is possible to plot it given the available data 
- the graph you are looking for cannot be created given the available data

This work tries to tackle the problem above. The workflow is as follows: 
1. Given a question, an LLM decides which one of the three scenarios stated above is valid
2. If it is possible to answer the question using available graphs, then that graph is retrieved and shown
3. If it is possible to answer the question using available graphs but, it is possible to create it using available data, then the SQL query that generated the data for the graph is created
4. If it is impossible to answer the question using available data, then this is stated

How to start the dashboard: 
1. add your openai api-key to an .env file `openai-api-key=<KEY>`
2. `pip install -r requirements.txt`
3. `streamlit run main.py`
