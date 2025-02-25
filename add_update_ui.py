import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

def add_update_tab():
    selected_date = st.date_input("Enter Date", datetime(2024, 8, 1))
    selected_date_str = selected_date.strftime("%Y-%m-%d")  # Format date for API

    # Fetch existing expenses
    response = requests.get(f"{API_URL}/expenses/{selected_date_str}")
    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="expense_form"):
        st.write("### Enter Expenses")

        expenses = []  # List to store user inputs

        for i in range(5):  # Allow up to 5 expense entries
            col1, col2, col3 = st.columns(3)

            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes = existing_expenses[i]['notes']
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            with col1:
                amount_input = st.number_input(
                    label=f"Amount {i + 1}",
                    min_value=0.0,
                    step=1.0,
                    value=amount,
                    key=f"amount_{i}"
                )
            with col2:
                category_input = st.selectbox(
                    label=f"Category {i + 1}",
                    options=categories,
                    index=categories.index(category),
                    key=f"category_{i}"
                )
            with col3:
                notes_input = st.text_input(
                    label=f"Notes {i + 1}",
                    value=notes,
                    key=f"notes_{i}"
                )

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button("Submit Expenses")

        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]  # Remove empty expenses

            response = requests.post(
                f"{API_URL}/expenses/{selected_date_str}",
                json=filtered_expenses
            )

            if response.status_code in [200, 201]:  # Handle successful responses
                st.success("Expenses updated successfully!")
            else:
                st.error(f"Failed to update expenses: {response.text}")  # Show error details

