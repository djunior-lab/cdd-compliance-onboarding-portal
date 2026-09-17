import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import datetime

# Database Connection via Streamlit Cloud Secrets (Falls back to local SQLite for testing)
DB_CONNECTION_STRING = st.secrets.get("DB_URL", "sqlite:///compliance_onboarding.db")
engine = create_engine(DB_CONNECTION_STRING)

st.set_page_config(page_title="FICA CDD & Compliance Operations Portal", layout="wide")

# Sidebar Navigation / Role Selector
st.sidebar.title("Navigation & Access")
portal_mode = st.sidebar.selectbox(
    "Select Portal View",
    ["Client Intake Portal", "FICA Compliance Team Dashboard"]
)

# -------------------------------------------------------------------------
# VIEW 1: CLIENT INTAKE PORTAL
# -------------------------------------------------------------------------
if portal_mode == "Client Intake Portal":
    st.title("Client Due Diligence (CDD) Intake Portal")
    st.write("Please complete the required compliance questionnaire and upload the mandatory supporting documents below to initiate your onboarding process.")

    client_category = st.selectbox(
        "Select Client Classification Type *",
        [
            "Natural Persons", 
            "Legal Persons (Private Companies, Close Corporations & Non-Profits)", 
            "Trusts", 
            "Foreign Companies & Other Legal Persons (Partnerships / Foreign Entities)"
        ]
    )

    with st.form("client_cdd_onboarding_form"):
        
        # Initialize file tracking metadata variables
        uploaded_file_names = "None"

        if client_category == "Natural Persons":
            st.subheader("1. Personal Particulars")
            full_name = st.text_input("Full Legal Name(s) and Surname *")
            dob = st.date_input("Date of Birth *", value=datetime.date(1990, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
            id_number = st.text_input("SA Identity Number (or Foreign Passport Number if non-resident) *")
            nationality = st.text_input("Nationality / Country of Residence *")
            
            st.subheader("2. Contact & Address Details")
            residential_address = st.text_area("Residential Address (Main place of domicile) *")
            mobile_number = st.text_input("Contact Numbers — Mobile *")
            email = st.text_input("Email Address *")
            
            st.subheader("3. Employment & Source of Funds")
            employment_status = st.selectbox("Employment Status", ["Employed", "Self-Employed", "Retired", "Unemployed"])
            occupation_employer = st.text_input("Occupation & Employer Name")
            source_of_funds = st.text_input("Source of Funds / Wealth for this transaction *")
            
            st.subheader("4. Status Check (DPEP / FPEP / PIP)")
            is_pep = st.selectbox(
                "Do you or any immediate family member hold a prominent public or political function (DPEP/FPEP/PIP)?",
                ["No", "Yes"]
            )

            st.subheader("5. Mandatory Document Uploads")
            id_doc = st.file_uploader("Upload ID / Passport *", type=["pdf", "png", "jpg", "jpeg"])
            por_doc = st.file_uploader("Upload Proof of Residence (Not older than 3 months) *", type=["pdf", "png", "jpg", "jpeg"])

            registered_entity_name = full_name
            registration_number = id_number
            entity_type = "Natural Person"
            country_of_incorporation = nationality
            primary_operating_regions = "South Africa"
            industry_sector = f"Occupation: {occupation_employer}"
            has_qualifying_ubo = "N/A - Individual"
            
            doc_list = []
            if id_doc: doc_list.append(f"ID/Passport: {id_doc.name}")
            if por_doc: doc_list.append(f"Proof of Residence: {por_doc.name}")
            if doc_list: uploaded_file_names = ", ".join(doc_list)

        elif client_category == "Legal Persons (Private Companies, Close Corporations & Non-Profits)":
            st.subheader("1. Entity Details")
            registered_entity_name = st.text_input("Registered Entity Name *")
            registration_number = st.text_input("Registration Number *")
            registered_address = st.text_area("Operating Address *")
            tax_vat_number = st.text_input("Tax / VAT Registration Number")
            
            entity_type = st.selectbox(
                "Entity Classification",
                ["Private Company (Pty) Ltd", "Close Corporation (CC)", "Non-Profit Organization (NPO)"]
            )
            
            st.subheader("2. Beneficial Ownership & Control")
            ubo_details = st.text_area("Beneficial Owners / Shareholders (Names, ID/Passport, Holding %)")
            industry_sector = st.text_input("Industry Sector / Commercial Purpose *")
            country_of_incorporation = "South Africa"
            primary_operating_regions = st.text_input("Primary Operating Territories *", value="South Africa")
            has_qualifying_ubo = "Captured in UBO text"
            is_pep = st.selectbox("Are any directors or beneficial owners PEPs / PIPs?", ["No", "Yes"])
            source_of_funds = st.text_input("Source of Funds / Wealth *")

            st.subheader("3. Mandatory Document Uploads")
            founding_docs = st.file_uploader("Founding Documents (CIPC Registration, Constitution, etc.) *", type=["pdf", "zip"], accept_multiple_files=True)
            entity_por = st.file_uploader("Proof of Operating Address (Not older than 3 months) *", type=["pdf", "png", "jpg", "jpeg"])
            dir_ids = st.file_uploader("Directors ID / Passports *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
            dir_pors = st.file_uploader("Directors Proof of Residence (Not older than 3 months)*", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
            share_register = st.file_uploader("Signed & Dated Share Register / Organogram *", type=["pdf", "png", "jpg", "jpeg"])

            doc_list = []
            if founding_docs: doc_list.append(f"Founding Docs ({len(founding_docs)} files)")
            if entity_por: doc_list.append(f"Business PoR: {entity_por.name}")
            if dir_ids: doc_list.append(f"Director IDs ({len(dir_ids)} files)")
            if dir_pors: doc_list.append(f"Director PoRs ({len(dir_pors)} files)")
            if share_register: doc_list.append(f"Share Register: {share_register.name}")
            if doc_list: uploaded_file_names = ", ".join(doc_list)

        elif client_category == "Trusts":
            st.subheader("1. Trust Particulars")
            registered_entity_name = st.text_input("Name of Trust *")
            registration_number = st.text_input("Master’s Office Reference Number (IT Number) *")
            
            st.subheader("2. Controlling Parties")
            controlling_parties = st.text_area("Founders, Trustees, and Named Beneficiaries (Full Names) *")
            
            entity_type = "Corporate Trust"
            country_of_incorporation = "South Africa"
            primary_operating_regions = "South Africa"
            industry_sector = "Trust / Asset Holding"
            has_qualifying_ubo = "Trust Parties Documented"
            is_pep = st.selectbox("Are any Founders, Trustees or Beneficiaries PEPs / PIPs?", ["No", "Yes"])
            source_of_funds = st.text_input("Source of Trust Capital / Wealth *")

            st.subheader("3. Mandatory Document Uploads")
            trust_deed = st.file_uploader("Trust Deed *", type=["pdf"], accept_multiple_files=True)
            letter_of_authority = st.file_uploader("Letter of Authority (Master of the High Court) *", type=["pdf"], accept_multiple_files=True)
            trustee_founder_ids = st.file_uploader("IDs for Trustees, Beneficiaries, Settlors, Founder, Donor *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
            trustee_founder_pors = st.file_uploader("Proof of Residence (Not older than 3 months) for Trustees, Beneficiaries, etc. *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)

            doc_list = []
            if trust_deed: doc_list.append("Trust Deed")
            if letter_of_authority: doc_list.append("Letter of Authority")
            if trustee_founder_ids: doc_list.append(f"Trust Parties IDs ({len(trustee_founder_ids)} files)")
            if trustee_founder_pors: doc_list.append(f"Trust Parties PoRs ({len(trustee_founder_pors)} files)")
            if doc_list: uploaded_file_names = ", ".join(doc_list)

        else:
            st.subheader("Section D: Foreign Companies & Other Legal Persons")
            registered_entity_name = st.text_input("Registered Name *")
            country_of_incorporation = st.text_input("Country of Incorporation *")
            registration_number = st.text_input("Foreign Registration / Identification Number *")
            
            entity_type = st.selectbox("Entity Classification", ["Foreign Incorporated Company", "Business Partnership", "Other Foreign Entity"])
            industry_sector = st.text_input("Primary Commercial Purpose / Sector *")
            primary_operating_regions = st.text_input("Operating Territories *", value="International")
            has_qualifying_ubo = "Foreign UBOs Documented"
            is_pep = st.selectbox("Are controllers classified as PEPs / PIPs?", ["No", "Yes"])
            source_of_funds = st.text_input("Source of Funds / Capital Origin *")

            st.subheader("3. Mandatory Document Uploads")
            foreign_founding_docs = st.file_uploader("Founding Documents (Foreign Registration, Constitution) *", type=["pdf", "zip"], accept_multiple_files=True)
            foreign_entity_por = st.file_uploader("Proof of Foreign Business Address (Not older than 3 months) *", type=["pdf", "png", "jpg", "jpeg"])
            foreign_dir_ids = st.file_uploader("Directors / Partners ID / Passports *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
            foreign_dir_pors = st.file_uploader("Directors / Partners Proof of Residence *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
            foreign_share_register = st.file_uploader("Signed & Dated Share Register / Organogram *", type=["pdf", "png", "jpg", "jpeg"])

            doc_list = []
            if foreign_founding_docs: doc_list.append("Foreign Founding Docs")
            if foreign_entity_por: doc_list.append("Foreign PoR")
            if foreign_dir_ids: doc_list.append(f"Foreign Director IDs ({len(foreign_dir_ids)} files)")
            if foreign_dir_pors: doc_list.append(f"Foreign Director PoRs ({len(foreign_dir_pors)} files)")
            if foreign_share_register: doc_list.append("Foreign Share Register")
            if doc_list: uploaded_file_names = ", ".join(doc_list)

        submitted = st.form_submit_button("Submit CDD Onboarding Questionnaire")

    if submitted:
        if not registered_entity_name or not registration_number:
            st.error("Mandatory Field Error: Please enter both the Entity/Name and Registration/ID Number.")
        else:
            client_id = f"CLI-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            payload = {
                "client_id": [client_id],
                "registered_entity_name": [registered_entity_name],
                "registration_number": [registration_number],
                "entity_type": [entity_type],
                "country_of_incorporation": [country_of_incorporation],
                "primary_operating_regions": [str(primary_operating_regions)],
                "industry_sector": [industry_sector],
                "has_qualifying_ubo": [has_qualifying_ubo],
                "is_pep_involved": [is_pep],
                "jurisdiction_risk_rating": ["Pending Initial Review"],
                "source_of_funds": [source_of_funds],
                "uploaded_documents": [uploaded_file_names],
                "assigned_analyst": ["Unassigned Intake Queue"],
                "review_status": ["Pending Compliance Review"],
                "submission_timestamp": [datetime.datetime.now()]
            }
            
            df_payload = pd.DataFrame(payload)
            
            try:
                df_payload.to_sql("dim_cdd_onboarding_staging", con=engine, if_exists="append", index=False)
                st.success("Your CDD onboarding questionnaire and files have been securely transmitted!")
                st.info(f"Your Reference ID is: **{client_id}**. Please save this token to track your onboarding status.")
            except Exception as e:
                st.error(f"Transmission failure: {e}")

# -------------------------------------------------------------------------
# VIEW 2: FICA COMPLIANCE TEAM DASHBOARD (SECURED WITH USERNAME & PASSWORD)
# -------------------------------------------------------------------------
elif portal_mode == "FICA Compliance Team Dashboard":
    st.title("FICA Compliance Operations & Analyst Dashboard")
    st.write("Restricted area for compliance officers, AML analysts, and onboarding supervisors.")

    # Session State Initialization for Login
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "logged_in_user" not in st.session_state:
        st.session_state["logged_in_user"] = ""

    if not st.session_state["authenticated"]:
        st.subheader("Compliance Team Authentication")
        with st.form("login_form"):
            username_input = st.text_input("Username")
            password_input = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Sign In")
            
            if login_btn:
                # Authorized Compliance Users
                valid_users = {
                    "analyst": "compliance2026",
                    "admin": "admin2026"
                }
                
                if username_input in valid_users and valid_users[username_input] == password_input:
                    st.session_state["authenticated"] = True
                    st.session_state["logged_in_user"] = username_input
                    st.success("Authentication successful! Loading dashboard...")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
    else:
        # Logged-in Header & Logout
        col_head1, col_head2 = st.columns([3, 1])
        with col_head1:
            st.info(f"Logged in as: **{st.session_state['logged_in_user'].upper()}**")
        with col_head2:
            if st.button("Sign Out"):
                st.session_state["authenticated"] = False
                st.session_state["logged_in_user"] = ""
                st.rerun()
        
        try:
            # Fetch staging records from Supabase / database
            df_queue = pd.read_sql("SELECT * FROM dim_cdd_onboarding_staging", con=engine)
            
            if df_queue.empty:
                st.info("The compliance queue is currently empty. No submissions have been logged.")
            else:
                st.subheader("Incoming Client Submissions Queue")
                st.dataframe(df_queue, use_container_width=True)
                
                st.markdown("---")
                st.subheader("Client Case Review & Document Verification")
                
                selected_client = st.selectbox("Select Client Reference ID to Review", df_queue["client_id"].tolist())
                
                client_record = df_queue[df_queue["client_id"] == selected_client].iloc[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Entity Name:** {client_record['registered_entity_name']}")
                    st.write(f"**Registration / ID:** {client_record['registration_number']}")
                    st.write(f"**Classification:** {client_record['entity_type']}")
                    st.write(f"**Source of Funds:** {client_record['source_of_funds']}")
                with col2:
                    st.write(f"**PEP Involvement:** {client_record['is_pep_involved']}")
                    st.write(f"**Current Status:** {client_record['review_status']}")
                    st.write(f"**Submission Timestamp:** {client_record['submission_timestamp']}")
                
                # Document Verification Panel
                st.markdown("### 📂 Uploaded Supporting Documents")
                uploaded_docs_str = client_record.get('uploaded_documents', 'No documents recorded')
                if uploaded_docs_str and uploaded_docs_str != "None":
                    st.success(f"Attached Files: **{uploaded_docs_str}**")
                    st.info("Verification status: Documents successfully received and logged to intake staging pipeline.")
                else:
                    st.warning("No file metadata recorded for this entry.")

                st.markdown("---")
                st.markdown("### Update Review Decision")
                new_status = st.selectbox("Change Compliance Status", ["Pending Compliance Review", "Approved - Cleared", "Rejected - High Risk / PEP Mismatch", "More Information Requested (RFI)"])
                risk_rating = st.selectbox("Assign FICA Risk Rating", ["Low Risk", "Medium Risk", "High Risk / Enhanced Due Diligence Required"])
                
                if st.button("Commit Compliance Decision"):
                    with engine.begin() as conn:
                        conn.execute(
                            f"UPDATE dim_cdd_onboarding_staging SET review_status = '{new_status}', jurisdiction_risk_rating = '{risk_rating}' WHERE client_id = '{selected_client}'"
                        )
                    st.success(f"Case {selected_client} updated successfully! Status set to: {new_status}")
                    st.rerun()

        except Exception as db_error:
            st.warning(f"Database table check pending or empty: {db_error}")
