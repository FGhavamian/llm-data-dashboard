import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.chains import (
    invoke_feasibility_chain,
    invoke_graph_selection_chain,
    invoke_sql_query_chain,
)


@st.cache_data
def load_data():
    revenue = pd.read_csv("data/revenue.csv")
    revenue["date"] = pd.to_datetime(revenue["date"])

    cost = pd.read_csv("data/cost.csv")

    return revenue, cost


revenue, cost = load_data()


def make_input_field():
    st.subheader("User Input")
    user_input = st.text_area("Enter your text here:", height=200)

    return user_input


def make_revenue_plot():
    st.subheader("Revenue")
    fig, ax = plt.subplots()
    ax.plot(revenue["date"], revenue["revenue"], label="Revenue")
    ax.set_xlabel("Date")
    ax.legend()
    st.pyplot(fig)


def make_cost_plot():
    st.subheader("Costs")
    fig, ax = plt.subplots()
    ax.pie(cost["cost"], labels=cost["process"], autopct="%1.1f%%", startangle=90)
    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)


if __name__ == "__main__":
    question = make_input_field()

    if st.button("Submit"):
        is_feasible = invoke_feasibility_chain(question)
        st.write(f"It is {is_feasible} to answer this quetion using available data.")

        if is_feasible == "feasible":
            graph_id = invoke_graph_selection_chain(question)
            st.write(f"Use graph {graph_id}.")

            if graph_id == 1:
                make_revenue_plot()
            elif graph_id == 2:
                make_cost_plot()

        elif is_feasible == "partially feasible":
            sql_query = invoke_sql_query_chain(question)
            print(sql_query)

            st.write("Use following sql query")
            st.write(f"```sql{sql_query}```")
