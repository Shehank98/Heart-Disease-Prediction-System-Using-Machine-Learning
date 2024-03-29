import streamlit as st
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Heart Disease Prediction System")
st.header("Column Details")

# Streamlit's st.header function does not provide direct control over font size.
# However, you can use HTML and CSS within the st.markdown function to customize the font size.
# Define the HTML with inline CSS for font size

AGE = """<div style="font-size: 16px;">Age : Age in years</div>"""
SEX = """<div style="font-size: 16px;">sex : 1 = male; 0 = female</div>"""
CP = """<div style="font-size: 16px;">cp : chest pain type</div>"""
TRESTBPS = """<div style="font-size: 16px;">trestbps : resting blood pressure (in mm Hg on admission to the hospital)</div>"""
CHOL = """<div style="font-size: 16px;">chol : serum cholestoral in mg/dl</div>"""
FBS = """<div style="font-size: 16px;">fbs : (fasting blood sugar &gt; 120 mg/dl) (1 = true; 0 = false)</div>"""
RESTECG = """<div style="font-size: 16px;">restecg : resting electrocardiographic results</div>"""
THALACH = """<div style="font-size: 16px;">thalach : maximum heart rate achieved</div>"""
EXANG = """<div style="font-size: 16px;">exang : exercise induced angina (1 = yes; 0 = no)</div>"""
OLDPEAK = """<div style="font-size: 16px;">oldpeak : ST depression induced by exercise relative to rest</div>"""

# Render HTML using st.markdown
st.markdown(AGE, unsafe_allow_html=True)
st.markdown(SEX, unsafe_allow_html=True)
st.markdown(CP, unsafe_allow_html=True)
st.markdown(TRESTBPS, unsafe_allow_html=True)
st.markdown(CHOL, unsafe_allow_html=True)
st.markdown(FBS, unsafe_allow_html=True)
st.markdown(RESTECG, unsafe_allow_html=True)
st.markdown(THALACH, unsafe_allow_html=True)
st.markdown(EXANG, unsafe_allow_html=True)
st.markdown(OLDPEAK, unsafe_allow_html=True)


# st.header("Age : Age in years")
# st.header("Sex : Chest pain type")
# st.header("cp : Age in years")
# st.header("trestbps : resting blood pressure (in mm Hg on admission to the hospital)")
# st.header("chol : serum cholestoral in mg/dl")
# st.header("fbs : (fasting blood sugar &gt; 120 mg/dl) (1 = true; 0 = false)")
# st.header("restecg : resting electrocardiographic results")
# st.header("thalach : maximum heart rate achieved")
# st.header("exang : exercise induced angina (1 = yes; 0 = no)")
# st.header("oldpeak : ST depression induced by exercise relative to rest")


uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])


def get_dataset(uploaded_file):
    if uploaded_file is not None:
        # Load the dataset from the uploaded file
        data = pd.read_csv(uploaded_file)
        return data
    else:
        return None


# Assign the result of get_dataset to a variable
data = get_dataset(uploaded_file)

X = None
y = None

# Check if data is not None before proceeding
if data is not None:
    # Assuming that the last column is the target variable
    # Copy the DataFrame to avoid modifying the original
    X = data.drop(columns=data.columns[-1]).copy()
    y = data[data.columns[-1]]

    # st.write("Shape of dataset", X.shape)
    st.subheader("Dataset Information:")
    st.markdown(
        f"**Shape of Dataset :** {X.shape[0]} rows x {X.shape[1]} columns")
    st.markdown(f"**Number of Classes :** {len(np.unique(y))}")
    # st.markdown("Shape of Classes", len(np.unique(y)))

    classifire_name = st.sidebar.selectbox(
        "Select Classifier", ("KNN", "SVM", "Random Forest"))

    def add_parameter_ui(clf_name):
        params = dict()
        if clf_name == "KNN":
            K = st.sidebar.slider("K", 1, 15)
            params["K"] = K
        elif clf_name == "SVM":
            C = st.sidebar.slider("C", 0.01, 10.0)
            params["C"] = C
        else:
            max_depth = st.sidebar.slider("max_depth", 2, 15)
            n_estimator = st.sidebar.slider("n_estimator", 1, 100)
            params["max_depth"] = max_depth
            params["n_estimator"] = n_estimator

        return params

    params = add_parameter_ui(classifire_name)

    def get_classifire(clf_name, params):
        if clf_name == "KNN":
            clf = KNeighborsClassifier(n_neighbors=params["K"])
        elif clf_name == "SVM":
            clf = SVC(C=params["C"])
        else:
            clf = RandomForestClassifier(n_estimators=params["n_estimator"],
                                         max_depth=params["max_depth"],
                                         random_state=10)
        return clf

    clf = get_classifire(classifire_name, params)

    # classification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.2, random_state=10)

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    acc = accuracy_score(y_test, y_pred)

    st.subheader("Classifier Performance:")
    st.markdown(f"**Classifier name:** {classifire_name}")
    st.markdown(f"**Accuracy:** {acc:.2%}")
else:
    st.warning("Please upload a CSV file.")

tabs = st.tabs(["Make Prediction", "Charts"])
tab_prediction = tabs[0]

with tab_prediction:
    st.header("Make Prediction")

    input_fields = []
    for feature in X.columns if X is not None else []:
        input_value = st.number_input(
            f"Enter {feature}:", min_value=X[feature].min(), max_value=X[feature].max())
        input_fields.append(input_value)

    input_data = pd.DataFrame(
        [input_fields], columns=X.columns) if X is not None else None

    prediction = clf.predict(input_data) if input_data is not None else None

    # st.write("Prediction:", prediction)
    # Display prediction result
    if prediction is not None:
        if prediction == 1:
            # st.write("Prediction: The patient has a Heart Disease")
            st.markdown(
                "<p style='color:red;'>Warning: The patient has a heart disease. ⚠️</p>", unsafe_allow_html=True)
        else:
            st.write("Prediction: The patient is normal.")
    else:
        st.write("No input data provided for prediction.")

tab2 = tabs[1]

# visulization
with tab2:
    chart_select = st.selectbox(
        label="Select the Chart type",
        options=['Scatterplot', 'Histogram', 'Boxplot']
    )

    if data is not None and chart_select in ['Scatterplot', 'Histogram', 'Boxplot']:
        numeric_columns = list(data.select_dtypes(['float', 'int']).columns)

    if chart_select == 'Scatterplot':
        st.subheader('Scatterplot Settings')
        try:
            x_values = st.selectbox('X axis', options=numeric_columns)
            y_values = st.selectbox('Y axis', options=numeric_columns)
            plot = px.scatter(data_frame=data, x=x_values, y=y_values)
            st.write(plot)
        except Exception as e:
            print(e)
    if chart_select == 'Histogram':
        st.subheader('Histogram Settings')
        try:
            x_values = st.selectbox('X axis', options=numeric_columns)
            plot = px.histogram(data_frame=data, x=x_values)
            st.write(plot)
        except Exception as e:
            print(e)
    if chart_select == 'Boxplot':
        st.subheader('Boxplot Settings')
        try:
            x_values = st.selectbox('X axis', options=numeric_columns)
            y_values = st.selectbox('Y axis', options=numeric_columns)
            plot = px.box(data_frame=data, x=x_values, y=y_values)
            st.write(plot)
        except Exception as e:
            print(e)
