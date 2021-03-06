from pycaret.regression import load_model, predict_model
import streamlit as st
import pandas as pd
import numpy as np

model = load_model('deployment_26062020')

def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df['Label'][0]
    return predictions

def run():

    from PIL import Image
    image = Image.open('health-insurance.jpg')
    image_hospital = Image.open('hospital.jpg')

    st.image(image,use_column_width=False)

    st.sidebar.info('This app was created to predict patient medical charges')
    #st.sidebar.info("<h1 style='text-align: center; color: grey;'>Insurance Charges Predictor</h1>", unsafe_allow_html=True)
        
    add_selectbox = st.sidebar.selectbox(
    "How would you like to predict?",
    ("Online", "Batch"))
    st.sidebar.image(image_hospital)

    st.sidebar.success('Check [here]() for more info')

    st.markdown("<h1 style='text-align: center; color: grey;'>Insurance Charges Predictor</h1>", unsafe_allow_html=True)


    if add_selectbox == 'Online':

        age = st.number_input('Enter the age of the primary beneficiary', min_value=1, max_value=100, value=20)
        sex = st.selectbox('Enter the gender of the primary beneficiary', ['male', 'female'])
        bmi = st.number_input('Enter the BMI (body mass index) of the primary beneficiary', min_value=10, max_value=60, value=10)
        children = st.selectbox('Enter the number of dependents covered by insurance', [0,1,2,3,4,5,6,7,8,9,10])
        if st.checkbox('Is the beneficiary smoker?'):
            smoker = 'yes'
        else:
            smoker = 'no'
        region = st.selectbox('Enter the beneficiary residential area in the US', ['southwest', 'northwest', 'northeast', 'southeast'])

        output=""

        input_dict = {'age' : age, 'sex' : sex, 'bmi' : bmi, 'children' : children, 'smoker' : smoker, 'region' : region}
        input_df = pd.DataFrame([input_dict])

        if st.button("Compute your expenses"):
            output = predict(model=model, input_df=input_df)
            output = '$' + str(output)

        st.success('Here are your expenses: {}'.format(output))

    if add_selectbox == 'Batch':

        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model,data=data)
            st.write(predictions)

if __name__ == '__main__':
    run()