import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

def main():
    # Load data from Excel
    df = pd.read_excel('C:\\Users\\kaurm\\Downloads\\archive\\healthcare_dataset.xlsx')

    # Clean and prepare data
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]
    df['name'] = df['name'].str.title()  # Standardizing text data
    df['medical_condition'] = df['medical_condition'].str.capitalize()
    df['date_of_admission'] = pd.to_datetime(df['date_of_admission'])
    df['discharge_date'] = pd.to_datetime(df['discharge_date'])

    # Define age groups
    bins = [0, 18, 35, 65, 100]
    labels = ['0-18', '19-35', '36-65', '65+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    # Display the cleaned data
    print(df.head())

    # Analysis: Summary statistics and group by operations
    print(df['billing_amount'].describe())
    admission_type_analysis = df.groupby('admission_type')['billing_amount'].mean()
    print(admission_type_analysis)

    # Visualization: Plotting distribution of Billing Amounts
    plt.figure(figsize=(10, 6))
    sns.histplot(df['billing_amount'], kde=True)
    plt.title('Distribution of Billing Amounts')
    plt.xlabel('Billing Amount')
    plt.ylabel('Frequency')
    plt.show()

    # Visualization: Total Costs by Age Group
    total_costs_age = df.groupby('age_group')['billing_amount'].sum()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=total_costs_age.index, y=total_costs_age.values)
    plt.title('Total Costs by Age Group')
    plt.xlabel('Age Group')
    plt.ylabel('Total Costs')
    plt.show()

    # Visualization: Box Plot of Billing Amounts by Admission Type to Analyze Outliers
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='admission_type', y='billing_amount', data=df)
    plt.title('Billing Amounts by Admission Type')
    plt.xlabel('Admission Type')
    plt.ylabel('Billing Amount')
    plt.show()

    # Export cleaned data to MySQL
    engine = create_engine('mysql+mysqlconnector://root:Kimjungkook1@localhost/cost_analysis')
    df.to_sql(name='cleaned_patient_records', con=engine, index=False, if_exists='replace')

if __name__ == '__main__':
    main()
