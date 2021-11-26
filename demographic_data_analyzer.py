import pandas as pd

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    df_age_sex = df[['age', 'sex']]
    avg_age = df_age_sex.groupby('sex').mean()
    average_age_men = avg_age.loc['Male']['age']
    average_age_men = round(average_age_men, 1)

    # What is the percentage of people who have a Bachelor's degree?
    education = df['education']
    education_percentages = education.value_counts(normalize=True) * 100

    percentage_bachelors = education_percentages['Bachelors']
    percentage_bachelors = round(percentage_bachelors, 1) 

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    education_salary = df[['education', 'salary']]
    higher_education = education_salary[(education_salary['education']=='Bachelors') | 
                                        (education_salary['education']=='Masters') |
                                        (education_salary['education']=='Doctorate')]
    lower_education = education_salary[(education_salary['education']!='Bachelors') & 
                                       (education_salary['education']!='Masters') &
                                       (education_salary['education']!='Doctorate')]

    # percentage with salary >50K
    higher_education_percentages = higher_education.value_counts(normalize=True) * 100
    lower_education_percentages = lower_education.value_counts(normalize=True) * 100
    higher_education_rich = higher_education_percentages[:,'>50K'].sum()
    lower_education_rich = lower_education_percentages[:,'>50K'].sum()

    higher_education_rich = round(higher_education_rich, 1)
    lower_education_rich = round(lower_education_rich, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    min_workers_salary = df[['salary']][df['hours-per-week']==1]
    min_workers_percentage = min_workers_salary.value_counts(normalize=True) * 100

    rich_percentage = min_workers_percentage['>50K']

    # What country has the highest percentage of people that earn >50K?
    country_salary = df[['native-country', 'salary']]
    pop = country_salary['native-country'].value_counts()
    highest_earning = country_salary[country_salary['salary']=='>50K']
    highest_earning = highest_earning.drop('salary', axis=1)
    highest_earning = highest_earning.value_counts()
    highest_earning_percentages = {}
    for index, value in highest_earning.items():
        highest_earning_percentages[index] = 100 * value / pop.loc[index]
    highest_earning_percentages = pd.Series(highest_earning_percentages)

    temp_tuple = highest_earning_percentages.idxmax()
    highest_earning_country_percentage = highest_earning_percentages.max()

    highest_earning_country = ''.join(temp_tuple)
    highest_earning_country_percentage = round(highest_earning_country_percentage, 1)

    # Identify the most popular occupation for those who earn >50K in India.
    df_IN = df[['occupation', 'salary', 'native-country']]
    highest_earning_occupations = df_IN[(df_IN['salary']=='>50K') & 
                                        (df_IN['native-country']=='India')]
    highest_earning_occupations = highest_earning_occupations.drop(['salary'], axis=1)
    highest_earning_occupations = highest_earning_occupations.drop(['native-country'], axis=1)
    
    temp_tuple = highest_earning_occupations.value_counts().idxmax()
    top_IN_occupation = ''.join(temp_tuple)

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
