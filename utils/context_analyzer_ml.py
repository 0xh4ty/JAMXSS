import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer # type: ignore
from sklearn.tree import DecisionTreeClassifier # type: ignore
import html

def train_model():
    # Load the labeled HTML responses from the CSV file
    data = pd.read_csv('labeled_html_responses.csv')

    # Split the data into features (HTML content) and labels (contexts)
    X = data['HTML Content']
    y = data['Label']

    # Convert HTML content into feature vectors using CountVectorizer
    vectorizer = CountVectorizer()
    X_vectorized = vectorizer.fit_transform(X)

    # Train a Decision Tree classifier
    classifier = DecisionTreeClassifier()
    classifier.fit(X_vectorized, y)

    return classifier, vectorizer

def predict_context(html_response, classifier, vectorizer):
    html_response_escaped = html.escape(html_response)
    html_response_vectorized = vectorizer.transform([html_response_escaped])
    predicted_context = classifier.predict(html_response_vectorized)
    return predicted_context[0]

def predict_contexts_for_reflections(html_response_lines, reflections, classifier, vectorizer):
    reflection_contexts = []

    for reflection_param, reflection_value in reflections:
        for i, line in enumerate(html_response_lines):
            if reflection_value in line:
                # Extract the HTML content around the reflection
                context_lines = html_response_lines[max(0, i - 2):min(len(html_response_lines), i + 3)]
                context_html = '\n'.join(context_lines)

                # Predict the context for the reflection
                predicted_context = predict_context(context_html, classifier, vectorizer)

                # Append the reflection parameter and its predicted context to the list
                reflection_contexts.append((reflection_param, predicted_context))
                break

    return reflection_contexts