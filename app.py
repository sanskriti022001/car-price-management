import streamlit as st
import pickle
import numpy as np
import pandas as pd
import traceback

model = pickle.load(open('car_price_prediction.pkl','rb'))

def main():
    string = "Car Price Predictor"
    st.set_page_config(page_title=string) 
    st.title("Car Price Predictor")
    st.markdown("Are you planning to sell your car?\n So let's try evaluating the price. ")
    st.image(
            "https://imgd.aeplcdn.com/0x0/n/cw/ec/27032/s60-exterior-right-front-three-quarter-3.jpeg",
            width=400, # Manually Adjust the width of the image as per requirement
        )
    st.write('')
    st.write('')
    years = st.number_input('In which year car was purchased ?',1990, 2022, step=1, key ='year')
    Years_old = 2022-years

    mileage = st.number_input('What is the mileage that the car gives?',1.0, 30.0, step=1.0, key ='mileage')
    Kms_Driven = st.number_input('What is distance completed by the car in Kilometers ?', 0.00, 500000.00, step=500.00, key ='drived')
    torque_log = st.number_input('Torgue', step=0.1, key ='torgue')
    seater = st.number_input('How many seats does the car have?', 1.0, 5.0, step=1.0, key ='seater')
    engine_op_number_sqaure = st.number_input('What is the engine operating number square?', 0.00, 100.00, step=0.5, key ='engine_op_number_sqaure')
    max_power_number_sqaure = st.number_input('What is the power of the engine in number square?', 0.00, 100.00, step=0.5, key ='max_power_number_sqaure')
    Car_age_log = st.number_input('How old is the car?', 0.0, 10.0, step=1.0, key ='car_age')
    
    # Fuel Type
    Fuel_Type_fuel = st.selectbox('What is the fuel type of the car ?',('Petrol','Diesel', 'CNG'), key='fuel')
    Fuel_Type_Petrol=0
    Fuel_Type_Diesel=0
    Fuel_Type_CNG=0
    
    if(Fuel_Type_fuel=='Petrol'):
        Fuel_Type_Petrol=1
    elif(Fuel_Type_fuel=='Diesel'):
        Fuel_Type_Diesel=1
    else:
        Fuel_Type_CNG = 1

    Seller_Type_Individual = st.selectbox('Are you a dealer or an individual ?', ('Dealer','Individual'), key='dealer')
    if(Seller_Type_Individual=='Individual'):
        Seller_Type_Individual=1
    else:
        Seller_Type_Individual=0	

    Present_Price = st.number_input('What is the current ex-showroom price of the car ?  (In ₹lakhs)', 0.00, 50.00, step=0.5, key ='present_price')
    
    Transmission_Mannual = st.selectbox('What is the Transmission Type ?', ('Manual','Automatic'), key='manual')
    if(Transmission_Mannual=='Mannual'):
        Transmission_Mannual=1
    else:
        Transmission_Mannual=0

    Owner = st.radio("The number of owners the car had previously ?", (0, 1, 2, 3, "4+"), key='owner')
    # [4+, 2, 1, 3]
    a = 0
    b = 0
    c = 0
    d = 0
    owner_val = [0, 0, 0, 0]
    if (Owner == 1):
        a = 0
        b = 0
        c = 1
        d = 0
    elif (Owner == 2):
        a = 0
        b = 1
        c = 0
        d = 0
    elif (Owner == 3):
        a = 0
        b = 0
        c = 0
        d = 1
    elif (Owner == 4):
        a = 1
        b = 0
        c = 0
        d = 0

    
    seller_type_Trustmark_Dealer = 0

    if st.button("Estimate Price", key='predict'):
        try:
            Model = model  #get_model()           
            features = np.array([[
                mileage, 
                Kms_Driven, 
                torque_log, 
                seater, 
                engine_op_number_sqaure, 
                max_power_number_sqaure,
                Car_age_log,
                Fuel_Type_Diesel,
                Fuel_Type_CNG,
                Fuel_Type_Petrol,
                Seller_Type_Individual,
                not Seller_Type_Individual,
                Transmission_Mannual,
                a, b, c, d
            ]])
            datafr = pd.DataFrame(features, columns=["mileage_number", "km_driven_sqaure", "torque_log","seats","engine_op_number_sqaure","max_power_number_sqaure","Car_age_log","fuel_Diesel","fuel_LPG","fuel_Petrol","seller_type_Individual","seller_type_Trustmark Dealer","transmission_Manual","owner_Fourth & Above Owner","owner_Second Owner","owner_Test Drive Car", "owner_Third Owner"])
            prediction = Model.predict(datafr)
            output = round(prediction[0],2)
            if output<0:
                st.warning("You will be not able to sell this car !!")
            else:
                st.success("You can sell the car for {} lakhs 🙌".format(output))
        except Exception as e:
            print(traceback.format_exc())
            st.warning("Opps!! Something went wrong\nTry again")
            # st.warning("Error: {}".format(e))


if __name__ == '__main__':
    main()