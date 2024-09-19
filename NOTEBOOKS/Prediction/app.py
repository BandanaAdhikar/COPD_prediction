# import the lbraries
import pandas as pd
import pickle 
import streamlit as st 

#load the trained model
with open('Best_Random_Forest_Model.pkl','rb')as f:
    model = pickle.load(f)

    #streamlit App
    def main():
        st.title("COPD Prediction Dashboard")

        #User input
        st.sidebar.header("User Input")

        age= st.sidebar.slider("Age", 30, 80, 50)
        gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
        bmi= st.sidebar.slider("BMI", 10, 40, 25)
        smoking_status = st.sidebar.selectbox("Smoking Status", ["Current", "Former", "Never"])
        biomass_fuel_exposre = st.sidebar.selectbox("Biomass Fuel Exposure", ["Yes", "No"])
        occupational_exposure = st.sidebar.selectbox("Occupational Exposure", ["Yes", "No"])
        family_history = st.sidebar.selectbox("Family History", ["Yes", "No"])
        air_pollution_level = st.sidebar.slider("Air pollution level", 0, 300, 50)
        respiratory_infections = st.sidebar.selectbox("Respiratory Infection In Children", ["", ""])
        location = st.sidebar.selectbox("Location", ["Kathmandu", "Pokhara", "Biratnagar", "Lalitpur", "Birgunj",'Chitwan' ,])

        # Process the input data
        input_data={
            'Age' : [age],
            'Gender' :[gender],
            'BMI': [bmi],
            'Smoking Status': [smoking_status],
            'Biomass Fuel Exposure': [biomass_fuel_exposre],
            'Occupational Exposure': [biomass_fuel_exposre],
            'Family History_COPD': [family_history],
            'Air Pollution Level': [air_pollution_level],
            'Respiratory Infections': [respiratory_infections],
            'Location':[location],
        }

        #Convert the data to a dataframe
        input_df = pd.DataFrame(input_data)

        #Encoding
        input_df['Gender'] = input_df["Gender"].map({'Male':1, 'Female':0})
        input_df['Smoking_status'] = input_df["Smoking_status"].map({'Current':1, 'Former':0.5, 'Never':0})
        input_df['Biomass_fuel_exposure'] = input_df["Biomass_fuel_exposure"].map({'Yes':1, 'No':0})
        input_df['Family_history_COPD'] = input_df["Family_history"].map({'Yes':1, 'No':0})
        input_df['Respiratory_infections'] = input_df["Respiratory_infections"].map({'Yes':1, 'No':0})
        input_df = pd.get_dummies(input_df, columns=['Location'], drop_first=True)
        location_dummies = pd.get_dummies(input_df['Location'],prefix ='Location')
        input_df = pd.concat([input_df, location_dummies],axis= 1)

        input_df.drop('Location',axis =1, inplace =True)

        #Prediction
        prediction = model.predict(input_df)
        if prediction[0] == 1:
            st.write("Predictions: COPD Detected")
        else:
            st.write("Predictions: No COPD Detected")

            if __name__ == "__main__":
                main()

