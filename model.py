import pandas as pd
import numpy as np


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


def model():
    train = train.drop(columns=dummy_list)
    validate = validate.drop(columns=dummy_list)
    test = test.drop(columns=dummy_list)
    

    x_train = train.drop(columns=['churn','customer_id'])
    y_train = train.churn

    x_validate = validate.drop(columns=['churn', 'customer_id'])
    y_validate = validate.churn

    x_test = test.drop(columns=['churn', 'customer_id'])
    y_test = test.churn


    RF1 = RandomForestClassifier(min_samples_leaf= 10, max_depth=10, random_state = 123)
    RF1.fit(x_train,y_train)
    y_pred = RF1.predict(x_train)

    train_score = RF1.score(x_train,y_train)
    validate_score = RF1.score(x_validate, y_validate)

    RF = RandomForestClassifier(min_samples_leaf=5, max_depth=6,random_state=123)
    RF.fit(x_train,y_train)
    y_proba = RF.predict_proba(x_test)
    y_pred = RF.predict(x_test)
    test_score = RF.score(x_test,y_test)

    print(f'Train: {train_score}, Validate: {validate_score}, Test: {test_score}')