import pickle
import streamlit as st

# loading the saved models
model = pickle.load(open('SVMmodel.sav', 'rb'))

def input_transformer(inputs):
    value_map = {
        "House Owned": {
            "Yes": 1,
            "No": 0
        },
        "Car Owned": {
            "Yes": 1,
            "No": 0
        },
        "Bike Owned": {
            "Yes": 1,
            "No": 0
        },
        "Has Active Loan": {
            "Yes": 1,
            "No": 0
        },
        "Client Income Type": {
          "Commercial": 1,
          "Service": 2,
          "Student": 3,
          "Retired": 4,
          "Unemployed": 5
        },
        "Client Education": {
          "Secondary": 1,
          "Graduation": 2
        },
        "Client Marital Status": {
          'Married': 1,
          'Widow': 2,
          'Single': 3,
          'Divorced':4
        },
        "Client Gender": {
          'Male': 1,
          'Female': 2
        },
        "Loan Contract Type": {
          'Cash Loan': 1,
          'Revolving Loan': 2
        }
    }

    transformed_inputs = []
    for input, value in inputs.items():
       if (value_map[input] != None and value_map[input][value] != None):
        transformed_inputs.append(value_map[input][value])

    return transformed_inputs

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1

# Function to go to the next step
def next_step():
    st.session_state.step += 1

# Function to go to the previous step
def prev_step():
    st.session_state.step -= 1

# Step 1: Input form
if st.session_state.step == 1:
    st.write("Step 1: Input Form")
    fName = st.text_input("Client full name: ")
    active_loan = st.selectbox("Already has an active loan?", ("-", "Yes", "No"))
    education = st.selectbox("Enter client education:", ("-", 'Secondary', 'Graduation'))
    employed_days = st.slider("Enter number of employed years before application:", min_value=0, max_value=80)
    income = st.text_input("Enter client income:", value=0)
    income_type = st.selectbox("Enter income type:", ("-", 'Commercial', 'Retired', 'Service', 'Student', 'Unemployed'))
    loan_contract_type = st.selectbox("Enter loan contract type:", ("-", 'Cash Loan', 'Revolving Loan'))
    loan_amount = st.text_input("Enter loan amount requested:", value=0)
    loan_annuity = st.text_input("Enter loan annuity amount:", value=0)
    age = st.slider("Enter age:", min_value=20, max_value=60)
    gender = st.selectbox("Enter client gender:", ("-", "Female", "Male"))
    child_count = st.selectbox("Enter child count:", (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    registration = st.slider("Years since registration:", min_value=0, max_value=50)
    marital_status = st.selectbox("Enter marital status:", ("-", "Divorced", "Single", "Married", "Widow"))
    car_owned = st.selectbox("Car owner?", ("-", "Yes", "No"))
    bike_owned = st.selectbox("Bike owner?", ("-", "Yes", "No"))
    house_owned = st.selectbox("House owner?", ("-", "Yes", "No"))

    if st.button('Next'):
        st.session_state.inputs = {
            "Loan Amount": loan_amount,
            "Income": income,
            "Loan Annuity": loan_annuity,
            "Age": age,
            "Child Count": child_count,
            "Employed Days": employed_days,
            "Years since registration": registration
        }
        st.session_state.inputs_to_transform = {
            "House Owned": house_owned,
            "Car Owned": car_owned,
            "Bike Owned": bike_owned,
            "Has Active Loan": active_loan,
            "Client Income Type": income_type,
            "Client Education": education,
            "Client Marital Status": marital_status,
            "Client Gender": gender,
            "Loan Contract Type": loan_contract_type
        }
        st.session_state.fName = fName
        next_step()

# Step 2: Validation and Prediction
elif st.session_state.step == 2:
    st.write("Step 2: Validation and Prediction")
    inputs = st.session_state.inputs
    inputs_to_transform = st.session_state.inputs_to_transform
    fName = st.session_state.fName
    invalid_inputs = []

    if fName.strip() == "":
        invalid_inputs.append("Client Name")

    if inputs["Loan Amount"].strip() == "0" or inputs["Loan Amount"].strip() == "":
        invalid_inputs.append("Loan Amount")

    for label, value in inputs.items():
        if value == '-' or value == "-" or value is None:
            invalid_inputs.append(label)

    for label, value in inputs_to_transform.items():
        if value == '-' or value == "-" or value is None:
            invalid_inputs.append(label)

    if len(invalid_inputs) > 0:
        invalid_inputs_str = "Following fields are invalid: \n"
        st.error(invalid_inputs_str + ", ".join(invalid_inputs))
    else:
        transformed_inputs = input_transformer(inputs_to_transform)
        inputs_array = [list(inputs.values()) + transformed_inputs]
        st.write("Client Name: " + fName)
        st.write("Loan Amount: " + inputs["Loan Amount"])
        prediction = model.predict(inputs_array)
        if prediction[0] == 0:
            st.success("Please accept the above loan request")
        else:
            st.error("Please reject the above request as client is more prone to default on the loan")

    if st.button('Back'):
        prev_step()
    if st.button('Submit'):
        st.write("Form submitted successfully!")