import acquire
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# import splitting and imputing functions
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

# turn off pink boxes for demo
import warnings
warnings.filterwarnings("ignore")


def prep_iris(df):
    df = df.drop(columns='species_id')
    df = df.rename(columns={'species_name':'species'})
    dummies = pd.get_dummies(df['species'], drop_first=True)
    df = pd.concat([df,dummies], axis=1)

    return(df)

def fill_age(df):
    train, test = train_test_split(df, test_size = .2, random_state=123, stratify=df.survived)
    train, validate = train_test_split(train, test_size=.25, random_state=123, stratify=train.survived)

    imputer = SimpleImputer(strategy='most_frequent')
    imputer = imputer.fit(train[['age']])

    train[['age']] = imputer.transform(train[['age']])

    validate[['age']] = imputer.transform(validate[['age']])

    test[['age']] = imputer.transform(test[['age']])

    df = pd.concat([train,validate,test])
    return(df)


def fill_embark(df):
    train, test = train_test_split(df, test_size = .2, random_state=123, stratify=df.survived)
    train, validate = train_test_split(train, test_size=.25, random_state=123, stratify=train.survived)

    imputer = SimpleImputer(strategy='most_frequent')
    imputer = imputer.fit(train[['embark_town']])

    train[['embark_town']] = imputer.transform(train[['embark_town']])

    validate[['embark_town']] = imputer.transform(validate[['embark_town']])

    test[['embark_town']] = imputer.transform(test[['embark_town']])

    df = pd.concat([train,validate,test])
    return(df)

def prep_titanic(df):
    df = df.drop(columns=['passenger_id','class','deck','embarked'])
    df = fill_embark(df)
    df = fill_age(df)
    dummies = pd.get_dummies(df[['sex','embark_town']], dummy_na=False, drop_first=[True, True])
    df = pd.concat([df, dummies],axis=1)
    df = df.drop(columns=['sex','embark_town'])
    train, test = train_test_split(df, test_size = .2, random_state=123, stratify=df.survived)
    train, validate = train_test_split(train, test_size=.25, random_state=123, stratify=train.survived)

    return(train,validate,test)


def prep_telco(df):
    #dropping blank rows
    df['total_charges'] = df["total_charges"].replace(' ', np.nan).astype(float)
    df = df.dropna()
    # removing protect class info from dataframe.
    df = df.drop(columns=['gender','senior_citizen','partner','dependents'])
    #removing duplicate columns
    df = df.drop(columns=['payment_type_id','internet_service_type_id','contract_type_id'])
    #creating a dummy list
    dummy_list = ['paperless_billing','online_security', 'online_backup','device_protection', 'streaming_tv', 'streaming_movies','multiple_lines','phone_service','tech_support','contract_type','internet_service_type','payment_type']
    #generating dummies
    dummies = dummies = pd.get_dummies(df[['paperless_billing','online_security', 'online_backup','device_protection', 'streaming_tv', 'streaming_movies','multiple_lines','phone_service','tech_support','contract_type','internet_service_type','payment_type']], dummy_na=False, drop_first=[True])
    df = pd.concat([df,dummies],axis=1)
    #splitting to account for data leakage
    train, test = train_test_split(df, test_size = .2, random_state=123, stratify=df.churn)
    train, validate = train_test_split(train, test_size=.25, random_state=123, stratify=train.churn)
    return(train,validate,test,dummy_list)

def important_variables(train):
    a = .05
    for variable in train:
    # we are checking each of the categorical variables for a dependent relationship with churn by using the chi^2
    # test. a p-score lower than .05 means the variable are likely statistically dependent.
        if train[variable].dtype == 'O':
            contract_churn = pd.crosstab(train[variable], train.churn)
            chi2, p, degf, expected = stats.chi2_contingency(contract_churn)
            chi2, p

            if p > a:
                print(f'{variable} and churn are NOT dependent.')
                
    # all of the continuous variable with the float64 type are ones where we want to know if the value
    # is higher for people who churn. so we are using a 1 tailed t-test, and looking for a t-score above 0
        elif train[variable].dtype == 'float64':
            churn_sample = train[train.churn == 'Yes'][variable]
            overall_mean = train[variable].mean()

            t, p = stats.ttest_1samp(churn_sample, overall_mean)
       
            if (p/2) > a:
                print(f'{variable} is NOT HIGHER for people who churn.')
            elif t<0:
                print(f'{variable} is NOT HIGHER for people who churn.')
            else:
                print(f'{variable} is HIGHER for people who churn. Confidence level: {1-(p/2)}')
    # tenure is the only variable left with the int64 type, and 
    # is also the only variable where we want to see if its value is lower for people who churn.
    # so we are still doing a 1-tailed t-test, but now we are looking for a t-score below 0
        elif train[variable].dtype == 'int64':
            churn_sample = train[train.churn == 'Yes'][variable]
            overall_mean = train[variable].mean()
            
            t,p = stats.ttest_1samp(churn_sample, overall_mean)
            
            if (p/2) > a:
                print(f'{variable} is NOT LOWER for people who churn.')
            elif t>0:
                print(f'{variable} is NOT LOWER for people who churn.')
            else:
                print(f'{variable} is LOWER for people who churn. Confidence level: {1-(p/2)}')
                