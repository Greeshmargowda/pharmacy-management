import streamlit as st
import pandas as pd
from PIL import Image
import random
import sqlite3

# Database connection
conn = sqlite3.connect("drug_data.db", check_same_thread=False)
c = conn.cursor()

# Functions to manage database
def cust_create_table():
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS Customers(
                        C_Name VARCHAR(50) NOT NULL,
                        C_Password VARCHAR(50) NOT NULL,
                        C_Email VARCHAR(50) PRIMARY KEY NOT NULL, 
                        C_State VARCHAR(50) NOT NULL,
                        C_Number VARCHAR(50) NOT NULL 
                        )''')
        conn.commit()
        st.success('Customer Table created Successfully')
    except Exception as e:
        st.error(f"Error creating Customer table: {e}")

def customer_add_data(Cname, Cpass, Cemail, Cstate, Cnumber):
    try:
        c.execute('''INSERT INTO Customers (C_Name, C_Password, C_Email, C_State, C_Number) VALUES (?, ?, ?, ?, ?)''', 
                  (Cname, Cpass, Cemail, Cstate, Cnumber))
        conn.commit()
    except Exception as e:
        st.error(f"Error adding customer: {e}")

def customer_view_all_data():
    c.execute('SELECT * FROM Customers')
    customer_data = c.fetchall()
    return customer_data

def customer_update(Cemail, Cnumber):
    try:
        c.execute('''UPDATE Customers SET C_Number = ? WHERE C_Email = ?''', (Cnumber, Cemail))
        conn.commit()
        st.success("Customer details updated")
    except Exception as e:
        st.error(f"Error updating customer: {e}")

def customer_delete(Cemail):
    try:
        c.execute('''DELETE FROM Customers WHERE C_Email = ?''', (Cemail,))
        conn.commit()
        st.success("Customer deleted")
    except Exception as e:
        st.error(f"Error deleting customer: {e}")

def drug_create_table():
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS Drugs(
                    D_Name VARCHAR(50) NOT NULL,
                    D_ExpDate DATE NOT NULL, 
                    D_Use VARCHAR(50) NOT NULL,
                    D_Qty INT NOT NULL, 
                    D_id INT PRIMARY KEY NOT NULL)
                    ''')
        conn.commit()
        st.success('Drug Table created Successfully')
    except Exception as e:
        st.error(f"Error creating Drugs table: {e}")

def drug_add_data(Dname, Dexpdate, Duse, Dqty, Did):
    try:
        c.execute('''INSERT INTO Drugs (D_Name, D_Expdate, D_Use, D_Qty, D_id) VALUES (?, ?, ?, ?, ?)''', 
                  (Dname, Dexpdate, Duse, Dqty, Did))
        conn.commit()
        st.success("Successfully Added Drug")
    except Exception as e:
        st.error(f"Error adding drug: {e}")

def drug_view_all_data():
    c.execute('SELECT * FROM Drugs')
    drug_data = c.fetchall()
    return drug_data

def drug_update(Duse, Did):
    try:
        c.execute('''UPDATE Drugs SET D_Use = ? WHERE D_id = ?''', (Duse, Did))
        conn.commit()
        st.success("Drug details updated")
    except Exception as e:
        st.error(f"Error updating drug: {e}")

def drug_delete(Did):
    try:
        c.execute('''DELETE FROM Drugs WHERE D_id = ?''', (Did,))
        conn.commit()
        st.success("Drug deleted")
    except Exception as e:
        st.error(f"Error deleting drug: {e}")

def order_create_table():
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS Orders(
                    O_Name VARCHAR(100) NOT NULL,
                    O_Items VARCHAR(100) NOT NULL,
                    O_Qty VARCHAR(100) NOT NULL,
                    O_id VARCHAR(100) PRIMARY KEY NOT NULL)
                    ''')
        conn.commit()
        st.success('Orders Table created Successfully')
    except Exception as e:
        st.error(f"Error creating Orders table: {e}")

def order_add_data(O_Name, O_Items, O_Qty, O_id):
    try:
        c.execute('''INSERT INTO Orders (O_Name, O_Items, O_Qty, O_id) VALUES (?, ?, ?, ?)''', 
                  (O_Name, O_Items, O_Qty, O_id))
        conn.commit()
        st.success("Order placed successfully")
    except Exception as e:
        st.error(f"Error adding order: {e}")

def order_view_data(customername):
    c.execute('SELECT * FROM Orders WHERE O_Name = ?', (customername,))
    order_data = c.fetchall()
    return order_data

def order_view_all_data():
    c.execute('SELECT * FROM Orders')
    order_all_data = c.fetchall()
    return order_all_data

def order_delete(Oid):
    try:
        c.execute('''DELETE FROM Orders WHERE O_id = ?''', (Oid,))
        conn.commit()
        st.success("Order deleted")
    except Exception as e:
        st.error(f"Error deleting order: {e}")

def get_authenticate(username, password):
    c.execute('SELECT C_Password FROM Customers WHERE C_Name = ?', (username,))
    cust_password = c.fetchone()
    if cust_password and cust_password[0] == password:
        return True
    else:
        return False

def customer_dashboard(username, password):
    if get_authenticate(username, password):
        st.title("Welcome to Pharmacy Store")

        st.subheader("Your Order Details")
        order_result = order_view_data(username)
        with st.expander("View All Order Data"):
            order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID"])
            st.dataframe(order_clean_df)

        drug_result = drug_view_all_data()
        st.subheader("Available Drugs")
        for i, drug in enumerate(drug_result):
            st.subheader(f"Drug: {drug[0]}")
            img_path = f'images/{drug[0].replace(" ", "").lower()}.jpg'
            try:
                img = Image.open(img_path)
                st.image(img, width=100, caption=f"Rs. {random.randint(10, 100)}/-")
            except FileNotFoundError:
                st.warning(f"Image for {drug[0]} not found")

            qty = st.slider(label=f"Quantity ({drug[0]})", min_value=0, max_value=5, key=i)
            st.info(f"When to USE: {drug[2]}")

            if qty > 0 and st.button(label="Buy now", key=f"buy_{i}"):
                O_items = drug[0]
                O_Qty = str(qty)
                O_id = username + "#O" + str(random.randint(0, 1000000))
                order_add_data(username, O_items, O_Qty, O_id)

def admin_dashboard():
    st.title("Pharmacy Database Dashboard")
    menu = ["Drugs", "Customers", "Orders", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Drugs":
        menu = ["Add", "View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Submenu", menu)
        if choice == "Add":
            st.subheader("Add Drugs")
            col1, col2 = st.columns(2)

            with col1:
                drug_name = st.text_area("Enter the Drug Name")
                drug_expiry = st.date_input("Expiry Date of Drug (YYYY-MM-DD)")
                drug_mainuse = st.text_area("When to Use")
            with col2:
                drug_quantity = st.number_input("Enter the quantity", min_value=0)
                drug_id = st.text_area("Enter the Drug ID (example:#D1)")

            if st.button("Add Drug"):
                drug_add_data(drug_name, drug_expiry, drug_mainuse, drug_quantity, drug_id)
        elif choice == "View":
            st.subheader("Drug Details")
            drug_result = drug_view_all_data()
            with st.expander("View All Drug Data"):
                drug_clean_df = pd.DataFrame(drug_result, columns=["Name", "Expiry Date", "Use", "Quantity", "ID"])
                st.dataframe(drug_clean_df)
            with st.expander("View Drug Quantity"):
                drug_name_quantity_df = drug_clean_df[['Name', 'Quantity']]
                st.dataframe(drug_name_quantity_df)
        elif choice == 'Update':
            st.subheader("Update Drug Details")
            d_id = st.text_area("Drug ID")
            d_use = st.text_area("Drug Use")
            if st.button('Update'):
                drug_update(d_use, d_id)
        elif choice == 'Delete':
            st.subheader("Delete Drugs")
            did = st.text_area("Drug ID")
            if st.button("Delete"):
                drug_delete(did)

    elif choice == "Customers":
        menu = ["View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Submenu", menu)
        if choice == "View":
            st.subheader("Customer Details")
            cust_result = customer_view_all_data()
            with st.expander("View All Customer Data"):
                cust_clean_df = pd.DataFrame(cust_result, columns=["Name", "Password", "Email-ID", "Area", "Number"])
                st.dataframe(cust_clean_df)
        elif choice == 'Update':
            st.subheader("Update Customer Details")
            cust_email = st.text_area("Email")
            cust_number = st.text_area("Phone Number")
            if st.button('Update'):
                customer_update(cust_email, cust_number)
        elif choice == 'Delete':
            st.subheader("Delete Customer")
            cust_email = st.text_area("Email")
            if st.button("Delete"):
                customer_delete(cust_email)

    elif choice == "Orders":
        menu = ["View"]
        choice = st.sidebar.selectbox("Submenu", menu)
        if choice == "View":
            st.subheader("Order Details")
            order_result = order_view_all_data()
            with st.expander("View All Order Data"):
                order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID"])
                st.dataframe(order_clean_df)

    elif choice == "About":
        st.subheader("DBMS Mini Project")
        st.subheader("By Aditi (226), Anweasha (235) & Vijay (239)")

# Main application
if __name__ == '__main__':
    drug_create_table()
    cust_create_table()
    order_create_table()

    menu = ["Login", "SignUp", "Admin"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            customer_dashboard(username, password)
    elif choice == "SignUp":
        st.subheader("Create New Account")
        cust_name = st.text_input("Name")
        cust_password = st.text_input("Password", type='password', key=1000)
        cust_password1 = st.text_input("Confirm Password", type='password', key=1001)
        col1, col2, col3 = st.columns(3)

        with col1:
            cust_email = st.text_area("Email ID")
        with col2:
            cust_area = st.text_area("State")
        with col3:
            cust_number = st.text_area("Phone Number")

        if st.button("Signup"):
            if cust_password == cust_password1:
                customer_add_data(cust_name, cust_password, cust_email, cust_area, cust_number)
                st.success("Account Created!")
                st.info("Go to Login Menu to login")
            else:
                st.warning("Passwords do not match")
    elif choice == "Admin":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if username == 'admin' and password == 'admin':
            admin_dashboard()

# Ensure database connection is closed
conn.close()
