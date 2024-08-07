# model_training.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def train_model(features, labels):
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def predict_stock_movement(model, current_data):
    return model.predict(current_data)

if __name__ == "__main__":
    # Example data
    features = pd.DataFrame({
        'sentiment_score': [0.1, 0.4, -0.3, 0.2, -0.5],
        'other_feature': [1, 2, 3, 4, 5]
    })
    labels = pd.Series([1, 0, 1, 0, 1])
    
    model = train_model(features, labels)
    current_data = pd.DataFrame({'sentiment_score': [0.2], 'other_feature': [3]})
    print(predict_stock_movement(model, current_data))
