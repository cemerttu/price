import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

class AIModel:
    def __init__(self, model_path='ai_model.pkl'):
        self.model_path = model_path
        self.model = None

    def train(self, csv_path, feature_cols, target_col):
        df = pd.read_csv(csv_path)
        X = df[feature_cols]
        y = df[target_col]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))
        joblib.dump(self.model, self.model_path)
        print(f"Model saved to {self.model_path}")

    def load(self):
        self.model = joblib.load(self.model_path)

    def predict(self, features):
        if self.model is None:
            self.load()
        return self.model.predict([features])[0]
