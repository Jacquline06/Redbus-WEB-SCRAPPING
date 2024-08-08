import pandas as pd
import mysql.connector
import streamlit as st
import base64

# Function to read binary file and encode it to base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Path to your image
background_image_path = 'E:/Project/Bus Project Automation/RedBusAutomation/img/AdobeStock_15537925_Preview.jpg'

# Convert the image to base64
base64_image = get_base64_of_bin_file(background_image_path)

# Set background image for Streamlit app
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{base64_image}");
    background-size: 30%;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
"""

# Inject CSS with markdown
st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("<center><h1>RED BUS APP</h1></center>", unsafe_allow_html=True)

# Function to connect to MySQL
def connect_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="busdetails"
        )
        print("Connected to MySQL database")
        return conn
    except Exception as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def objective():
    st.header("Objective")
    st.markdown("<h1 style='color: #3498db;'>Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit</h1>", unsafe_allow_html=True)

def required_python_libraries():
    st.header("Required Python Libraries")
    st.write("The following Python libraries are required for the project:")
    libraries = ["Selenium", "pandas", "streamlit", "mysql.connector", "datetime", "re"]
    libraries_html = "".join([f"<li style='color: #e74c3c;'>{lib}</li>" for lib in libraries])
    st.markdown(f"<ul>{libraries_html}</ul>", unsafe_allow_html=True)

def about():
    st.write(" The Redbus Data Scraping and Filtering with Streamlit Application aims to" 
             "revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry")

def developer():
    st.write("Emailid : cuttyjemimah@gmail.com")
    st.write("Name : Jacquline Jemimah")
    st.write("Language : python, java, spring")

st.sidebar.header("Navigation Menu")
menu_option = st.sidebar.radio("Choose a page:", ["Home", "Project"])

if menu_option == "Home":
    def main():
        # Main layout
        col1, col2 = st.columns(2)

        with col1:
            st.header("Navigation")
            options = ["Objective", "Required Python Libraries", "About", "Developer"]
            choice = st.radio("Go to", options)

        with col2:
            if choice == "Objective":
                objective()
            elif choice == "Required Python Libraries":
                required_python_libraries()
            elif choice == "About":
                about()
            elif choice == "Developer":
                developer()

    if __name__ == "__main__":
        main()

# The project starts from here
if menu_option == "Project":
    st.write("Bus is available only for Andhra state and Kerala")
    df = pd.read_csv("E:/Project/Bus Project Automation/RedBusAutomation/csv files/Allroute.csv")
    df1 = pd.read_csv("E:/Project/Bus Project Automation/RedBusAutomation/csv files/data.csv")
    
    range_values = st.slider("Select a range of values:", min_value=0, max_value=10000, value=(0, 10000))
    st.write("You selected a range:", range_values)
    
    bus_types = []
    
    # Connect to MySQL
    conn = connect_mysql()
    if conn:
        my_cursor = conn.cursor()
        
        # Fetch distinct bus types
        try:
            query = 'SELECT DISTINCT Bus_type FROM bus_routes'
            my_cursor.execute(query)
            result = my_cursor.fetchall()
            
            bus_types = [row[0] for row in result]

            if not bus_types:
                st.write("No bus types found.")
        except Exception as e:
            st.write(f"Error: {str(e)}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Apply for price sort"):
            st.write(f'The values between {range_values[0]} and {range_values[1]}')
            try:
                query = f'''
                    SELECT Bus_name, Start_time, Total_duration, End_time, Price, Ratings, Seats_Available, Bus_type, route_link 
                    FROM bus_routes 
                    WHERE Price BETWEEN {range_values[0]} AND {range_values[1]} 
                    ORDER BY Price DESC
                '''
                my_cursor.execute(query)
                out = my_cursor.fetchall()
                
                df = pd.DataFrame(out, columns=[
                    "Bus_name", "Start_time", "Total_duration", "End_time", "Price", "Ratings", "Seats_Available", "Bus_type", "route_link"
                ])
                
                st.write(df)
                st.write(f"Total number of records: {len(df)}")
            except Exception as e:
                st.write(f"Error: Fetching the database - {str(e)}")
    
    with col2:
        if st.button("Apply for seat available"):
            try:
                query = '''
                    SELECT Bus_name, Start_time, Total_duration, End_time, Price, Ratings, Seats_Available, Bus_type, route_link 
                    FROM bus_routes 
                    WHERE Seats_Available > 10
                '''
                my_cursor.execute(query)
                out = my_cursor.fetchall()
                
                df = pd.DataFrame(out, columns=[
                    "Bus_name", "Start_time", "Total_duration", "End_time", "Price", "Ratings", "Seats_Available", "Bus_type", "route_link"
                ])
                
                st.write(df)
                st.write(f"Total number of records: {len(df)}")
            except Exception as e:
                st.write(f"Error: Fetching the database - {str(e)}")
    
    with col3:
        selected_type = st.selectbox("Select Bus Type", ["All"] + bus_types)
        
        if st.button("Apply for Bus type"):
         #st.write(f"Showing results for bus type: {selected_type}")
            
         try:
                query = '''
                    SELECT Bus_name, Start_time, Total_duration, End_time, Price, Ratings, Seats_Available, Bus_type, route_link 
                    FROM bus_routes 
                    WHERE Seats_Available > 10
                '''
                
                if selected_type != "All":
                    query += f" AND Bus_type = '{selected_type}'"
                
                my_cursor.execute(query)
                out = my_cursor.fetchall()
                
                df = pd.DataFrame(out, columns=[
                    "Bus_name", "Start_time", "Total_duration", "End_time", "Price", "Ratings", "Seats_Available", "Bus_type", "route_link"
                ])
                
                st.write(df)
                st.write(f"Total number of records: {len(df)}")
         except Exception as e:
                 st.write(f"Error: Fetching the database - {str(e)}")

    try:
        #To display the count of the data fetched
        df()
    except:
        st.write ("Still DataFrame not fetched")        
