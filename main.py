import streamlit as st
import pickle
import numpy as np

# Load the model
with open("C:/Users/bhara/Desktop/PRO/src/Thyroid_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Define the prediction function
def predict_thyroid(Age, Sex, TSH, TT4, FTI, on_thyroxine, on_antithyroid_medication, goitre, hypopituitary, psych, T3_measured):
    # Convert categorical variables to numerical
    Sex = 1 if Sex == "Male" else 0
    on_thyroxine = 1 if on_thyroxine == "True" else 0
    on_antithyroid_medication = 1 if on_antithyroid_medication == "True" else 0
    goitre = 1 if goitre == "True" else 0
    hypopituitary = 1 if hypopituitary == "True" else 0
    psych = 1 if psych == "True" else 0
    T3_measured = 1 if T3_measured == "True" else 0
    
    # Make prediction
    arr = np.array([[Age, Sex, TSH, TT4, FTI, on_thyroxine, on_antithyroid_medication, goitre, hypopituitary, psych, T3_measured]])
    pred = model.predict(arr)

    if pred == 0:
        return "Compensated Hypothyroid"
    elif pred == 1:
        return "No Thyroid"
    elif pred == 2:
        return "Primary Hypothyroid"
    elif pred == 3:
        return "Secondary Hypothyroid"

# Streamlit app
def main():    
    # Input fields
    Age = st.number_input("Age")
    Sex = st.selectbox("Sex", ["Male", "Female"])
    TSH = st.number_input("Level of Thyroid Stimulating Hormone (TSH)")
    TT4 = st.number_input("Total Thyroxine (TT4)")
    FTI = st.number_input("Free Thyroxine Index (FTI)")
    on_thyroxine = st.selectbox("On Thyroxine", ["True", "False"])
    on_antithyroid_medication = st.selectbox("On Antithyroid Medication", ["True", "False"])
    goitre = st.selectbox("Goitre", ["True", "False"])
    hypopituitary = st.selectbox("Hypopituitary", ["True", "False"])
    psych = st.selectbox("Psychological Symptoms", ["True", "False"])
    T3_measured = st.selectbox("Is T3 measured?", ["True", "False"])

    if st.button("Predict"):
        prediction = predict_thyroid(Age, Sex, TSH, TT4, FTI, on_thyroxine, on_antithyroid_medication, goitre, hypopituitary, psych, T3_measured)
        st.write(f"Patient has {prediction}")

    def render_template(file_path):
        with open(file_path, "r") as f:
            template_content = f.read()
        return template_content



    # Include HTML templates
    st.markdown(render_template("C:/Users/bhara/Desktop/PRO/templates/home.html"), unsafe_allow_html=True)
    st.markdown(render_template("C:/Users/bhara/Desktop/PRO/templates/moreinfo.html"), unsafe_allow_html=True)
    st.markdown(render_template("C:/Users/bhara/Desktop/PRO/templates/predict.html"), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
