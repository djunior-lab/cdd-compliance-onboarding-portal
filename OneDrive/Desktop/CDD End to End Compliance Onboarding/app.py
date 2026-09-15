import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import datetime

# Database Connection (Initializes a local SQLite database file for portfolio testing)
DB_CONNECTION_STRING = "sqlite:///compliance_onboarding.db" 
engine = create_engine(DB_CONNECTION_STRING)

st.set_page_config(page_title="Client Onboarding Portal | FICA Compliance", layout="centered")

st.title("Client Due Diligence (CDD) Intake Portal")
st.write("Please complete the required compliance questionnaire and upload the mandatory supporting documents below to initiate your onboarding process.")

# Master Selection for Dynamic Conditional Rendering
client_category = st.selectbox(
    "Select Client Classification Type *",
    [
        "Natural Persons (Individuals)", 
        "Legal Persons (Private Companies, Close Corporations & Non-Profits)", 
        "Trusts", 
        "Foreign Companies & Other Legal Persons (Partnerships / Foreign Entities)"
    ]
)

with st.form("client_cdd_onboarding_form"):
    
    # ----------------------------------------------------
    # SECTION A: NATURAL PERSONS (INDIVIDUALS)
    # ----------------------------------------------------
    if client_category == "Natural Persons (Individuals)":
        st.subheader("Section A: Natural Persons (Individuals) - Personal Particulars")
        full_name = st.text_input("Full Legal Name(s) and Surname *")
        dob = st.date_input("Date of Birth *", value=datetime.date(1990, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        id_number = st.text_input("SA Identity Number (or Foreign Passport Number if non-resident) *")
        nationality = st.multiselect("Nationality", ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", 
                                                     "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", 
                                                     "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
                                                       "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", 
                                                       "Côte d'Ivoire", "Croatia", "Cuba", "Cyprus", "Czechia", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", 
                                                       "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", 
                                                       "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", 
                                                       "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", 
                                                       "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", 
                                                       "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", 
                                                       "Mauritania", "Mauritius", "Mexico", "Micronesia", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", 
                                                       "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", 
                                                       "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", 
                                                       "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", 
                                                       "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", 
                                                       "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", 
                                                       "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", 
                                                       "Vietnam", "Yemen", "Zambia", "Zimbabwe"])
        
        st.subheader("2. Contact & Address Details")
        residential_address = st.text_area("Residential Address (Main place of domicile — Note: P.O. Box is not accepted) *")
        mobile_number = st.text_input("Contact Numbers — Mobile *")
        work_number = st.text_input("Contact Numbers — Work")
        email = st.text_input("Email Address *")
        
        st.subheader("3. Employment & Source of Funds / Wealth")
        employment_status = st.selectbox("Employment Status", ["Employed", "Self-Employed", "Retired", "Unemployed"])
        occupation_employer = st.text_input("Occupation & Employer Name")
        source_of_funds = st.text_input("Source of Funds / Wealth for this transaction *")
        
        st.subheader("4. Status Check (DPEP / FPEP / PIP)")
        is_pep = st.selectbox(
            "Do you or any immediate family member / close associate currently—or within the past 12 months—hold a prominent public function or political position domestically (DPEP) or internationally (FPEP), or are you a Prominent Influential Person (PIP)?",
            ["No", "Yes"]
        )
        pep_details = st.text_input("If yes, please provide details of the position and relationship")

        st.subheader("5. Mandatory Document Uploads")
        id_doc = st.file_uploader("Upload ID / Passport *", type=["pdf", "png", "jpg", "jpeg"])
        por_doc = st.file_uploader("Upload Proof of Residence (Not older than 3 months) *", type=["pdf", "png", "jpg", "jpeg"])

        # Mapping fields for database staging
        registered_entity_name = full_name
        registration_number = id_number
        entity_type = "Natural Person"
        country_of_incorporation = ", ".join(nationality) if isinstance(nationality, list) else str(nationality)
        primary_operating_regions = "South Africa"
        industry_sector = f"Occupation: {occupation_employer}"
        has_qualifying_ubo = "N/A - Individual"

    # ----------------------------------------------------
    # SECTION B: LEGAL PERSONS
    # ----------------------------------------------------
    elif client_category == "Legal Persons (Private Companies, Close Corporations & Non-Profits)":
        st.subheader("Section B: Legal Persons - Entity Details")
        registered_entity_name = st.text_input("Registered Entity Name *")
        registration_number = st.text_input("Registration Number *")
        registered_address = st.text_area("Registered / Business Address *")
        tax_vat_number = st.text_input("Tax / VAT Registration Number")
        
        entity_type = st.selectbox(
            "Entity Classification",
            ["Private Company (Pty) Ltd", "Close Corporation (CC)", "Non-Profit Organization (NPO)"]
        )
        
        st.subheader("2. Beneficial Ownership & Control")
        st.write("Provide details of natural persons who independently or together hold a controlling ownership interest (typically 5% or more of voting rights or shares):")
        ubo_1 = st.text_input("Beneficial Owner 1 (Full Name, ID/Passport, Shareholding %)")
        ubo_2 = st.text_input("Beneficial Owner 2 (Full Name, ID/Passport, Shareholding %)")
        exec_management = st.text_area("Details of Executive Management / Directors (if different from beneficial owners)")
        
        country_of_incorporation = "South Africa"
        primary_operating_regions = st.multiselect("Primary Operating Territories", ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Côte d'Ivoire", "Croatia", "Cuba", "Cyprus", "Czechia", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"])
        industry_sector = st.text_input("Industry Sector / Commercial Purpose *")
        has_qualifying_ubo = "Captured in UBO fields"
        is_pep = st.selectbox("Are any directors or beneficial owners PEPs / PIPs?", ["No", "Yes"])
        source_of_funds = st.text_input("Source of Funds / Wealth *")

        st.subheader("3. Mandatory Document Uploads")
        founding_docs = st.file_uploader("Founding Documents (CIPC Registration, Constitution, etc.) *", type=["pdf", "zip"], accept_multiple_files=True)
        entity_por = st.file_uploader("Proof of Business Address (Not older than 3 months) *", type=["pdf", "png", "jpg", "jpeg"])
        dir_ids = st.file_uploader("Directors ID / Passports (Upload all directors) *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
        dir_pors = st.file_uploader("Directors Proof of Residence (Upload all directors) *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
        share_register = st.file_uploader("Signed & Dated Share Register / Organogram *", type=["pdf", "png", "jpg", "jpeg"])

    # ----------------------------------------------------
    # SECTION C: TRUSTS
    # ----------------------------------------------------
    elif client_category == "Section C: Trusts":
        st.subheader("Section C: Trusts - Trust Particulars")
        registered_entity_name = st.text_input("Official Name of Trust *")
        registration_number = st.text_input("Master’s Office where registered & Trust Registration / Reference Number (IT Number) *")
        
        st.subheader("2. Controlling Parties")
        founders = st.text_area("Founders / Settlors (Full Name(s)) *")
        trustees = st.text_area("All Active Trustees (Full Name(s)) *")
        beneficiaries = st.text_area("All Named Beneficiaries (Full Name(s)) *")
        
        entity_type = "Corporate Trust"
        country_of_incorporation = "South Africa"
        primary_operating_regions = st.multiselect("Operating Regions", ["South Africa", "International"])
        industry_sector = "Trust / Asset Holding"
        has_qualifying_ubo = "Trust Controlling Parties Documented"
        is_pep = st.selectbox("Are any Founders, Trustees or Beneficiaries PEPs / PIPs?", ["No", "Yes"])
        source_of_funds = st.text_input("Source of Trust Capital / Wealth *")

        st.subheader("3. Mandatory Document Uploads")
        trust_deed = st.file_uploader("Trust Deed *", type=["pdf"], accept_multiple_files=True)
        letter_of_authority = st.file_uploader("Letter of Authority (Master of the High Court) *", type=["pdf"], accept_multiple_files=True)
        trustee_founder_ids = st.file_uploader("IDs for Trustees, Beneficiaries, Settlors, Founder, Donor *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
        trustee_founder_pors = st.file_uploader("Proof of Residence (Not older than 3 months) for Trustees, Beneficiaries, Settlors, Founder, Donor *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)

    # ----------------------------------------------------
    # FOREIGN COMPANIES & OTHER LEGAL PERSONS
    # ----------------------------------------------------
    else:
        st.subheader("Section D: Foreign Companies & Other Legal Persons")
        registered_entity_name = st.text_input("Registered Name *")
        country_of_incorporation = st.text_input("Country of Incorporation *")
        registration_number = st.text_input("Registration / Identification Number issued abroad *")
        foreign_address = st.text_area("Foreign Registered / Principal Place of Business Address *")
        
        entity_type = st.selectbox("Entity Classification", ["Foreign Incorporated Company", "Business Partnership", "Other Foreign Entity"])
        
        st.subheader("2. Foreign Beneficial Ownership & Management")
        st.write("Identify all natural persons exercising ultimate effective control over the foreign entity or partnership:")
        foreign_controller_1 = st.text_input("Controller 1 (Name, Capacity/Role, Country of Residence)")
        foreign_controller_2 = st.text_input("Controller 2 (Name, Capacity/Role, Country of Residence)")
        
        industry_sector = st.text_input("Primary Commercial Purpose / Sector *")
        primary_operating_regions = st.multiselect("Operating Territories", ["South Africa", "International", "Cross-Border"])
        has_qualifying_ubo = "Foreign UBOs Documented"
        is_pep = st.selectbox("Are controllers classified as PEPs / PIPs?", ["No", "Yes"])
        source_of_funds = st.text_input("Source of Funds / Capital Origin *")

        st.subheader("3. Mandatory Document Uploads")
        foreign_founding_docs = st.file_uploader("Founding Documents (Foreign Registration, Constitution, etc.) *", type=["pdf", "zip"], accept_multiple_files=True)
        foreign_entity_por = st.file_uploader("Proof of Foreign Business Address (Not older than 3 months) *", type=["pdf", "png", "jpg", "jpeg"])
        foreign_dir_ids = st.file_uploader("Directors / Partners ID / Passports *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
        foreign_dir_pors = st.file_uploader("Directors / Partners Proof of Residence *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
        foreign_share_register = st.file_uploader("Signed & Dated Share Register / Organogram *", type=["pdf", "png", "jpg", "jpeg"])

    submitted = st.form_submit_button("Submit CDD Onboarding Questionnaire")

if submitted:
    if not registered_entity_name or not registration_number:
        st.error("Mandatory Field Error: Please enter both the Name/Entity Name and Registration/ID Number.")
    else:
        client_id = f"CLI-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        if isinstance(primary_operating_regions, list):
            operating_regions_str = ", ".join(primary_operating_regions)
        else:
            operating_regions_str = str(primary_operating_regions)

        payload = {
            "client_id": [client_id],
            "registered_entity_name": [registered_entity_name],
            "registration_number": [registration_number],
            "entity_type": [entity_type],
            "country_of_incorporation": [country_of_incorporation],
            "primary_operating_regions": [operating_regions_str],
            "industry_sector": [industry_sector],
            "has_qualifying_ubo": [has_qualifying_ubo],
            "is_pep_involved": [is_pep],
            "jurisdiction_risk_rating": ["Pending Initial Review"],
            "source_of_funds": [source_of_funds],
            "assigned_analyst": ["Unassigned Intake Queue"],
            "review_status": ["Pending Compliance Review"],
            "submission_timestamp": [datetime.datetime.now()]
        }
        
        df_payload = pd.DataFrame(payload)
        
        try:
            df_payload.to_sql("dim_cdd_onboarding_staging", con=engine, if_exists="append", index=False)
            st.success("Your CDD onboarding questionnaire and files have been securely transmitted!")
            st.info(f"Your Reference ID is: **{client_id}**. Our legal intake team will review your submission shortly.")
        except Exception as e:
            st.error(f"Transmission failure: {e}")
