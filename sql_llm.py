from langchain_groq import ChatGroq
import os
import pandas as pd

COLUMNS = ['Type', 'Stock', 'VIN', 'Year', 'Make', 'Model', 'Body', 'ModelNumber',
       'Doors', 'ExteriorColor', 'interiorColor', 'EngineCylinders',
       'EngineDisplacement', 'Transmission', 'Miles', 'SellingPrice', 'MSRP',
       'BookValue', 'Invoice', 'Certified', 'Options', 'Style_Description',
       'Ext_Color_Generic', 'Ext_Color_Code', 'int_Color_Generic',
       'int_Color_Code', 'int_Upholstery', 'Engine_Block_Type',
       'Engine_Aspiration_Type', 'Engine_Description', 'Transmission_Speed',
       'Transmission_Description', 'Drivetrain', 'Fuel_Type', 'CityMPG',
       'HighwayMPG', 'EPAClassification', 'Wheelbase_Code', 'internet_Price',
       'MarketClass', 'PassengerCapacity', 'ExtColorHexCode',
       'intColorHexCode', 'EngineDisplacementCubicInches']

QUANT_COLUMNS = {
        'Type': 'str', 'Year': pd.Int64Dtype(), 'Make': 'str', 'Body': 'str', 'Doors': pd.Int64Dtype(), 'EngineCylinders': pd.Int64Dtype(), 'Engine_Block_Type': 'str', 'Engine_Aspiration_Type': 'str', 'Transmission': 'str', 'Drivetrain': 'str', 'Fuel_Type': 'str', 'CityMPG': 'float', 'HighwayMPG': 'float', 'Miles':'float' , 'SellingPrice': 'float', 'Certified': 'bool', 'PassengerCapacity': pd.Int64Dtype()
}


# Initialize ChatGroq client
api_key = os.getenv('GROQ_API_KEY')
llm = ChatGroq(api_key=api_key)

def generate_query(user_prompt):
    # Define a structured prompt for the LLM
    prompt = f"""
    I have a database of cars for a dealership. Based on the user prompt, generate a safe SQLite3 query. 
    Ensure the query matches the user's intent without risking SQL injection or data corruption. 
    It has to be only the query no extra added comments so that your response can be used as the query directly.
    Here are the possible columns in the database: {COLUMNS} and {QUANT_COLUMNS}.
    Be very conservative and only use columns that are in the possible values dictionary.
    the database is "cars.db"
    
    User prompt: {user_prompt}
    
    Example input: "Show me all rows from the 'cars' table where the model is Mazda."
    Example output: SELECT * FROM cars WHERE Make == 'Mazda';
    """
    
    # Get the response from ChatGroq
    response = llm.invoke(prompt)
    return response.content