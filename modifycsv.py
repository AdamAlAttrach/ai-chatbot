import pandas as pd

def add_description_field():
    """
    Adds a 'description' field to the CSV file by concatenating all the column values for each row.
    Args:
        input_csv (str): Path to the input CSV file.
        output_csv (str): Path to save the updated CSV file with the 'description' field.
    """
    # Read the CSV file
    df = pd.read_csv('vehicles.csv')
    
    # Concatenate all column values into a single 'description' field
    df['description'] = df.apply(lambda row: ' '.join(map(str, row.values)), axis=1)
    
    # Save the updated DataFrame back to a new CSV file
    df.to_csv('vehicles.csv', index=False)


add_description_field()
