import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Data structures
rtb_combinations = {
    "AUT": [
        "Applied Mathematics B", "Automotive Engines", "Automotive Engine Auxillaries Systems",
        "Automotive Electrical and Electronic Systems", "Applied Physics B",
        "Automotive Transmission and Control Systems", "Automotive Body Works",
        "Ikinyarwanda", "English", "Applied Chemistry A", "Entrepreneurship",
        "Practical AUT"
    ],
    "WIR": [
        "Applied Mathematics B", "Topography and Technical Drawing", "Applied Biology A",
        "Construction and Maintenance of Surface Irrigation", "Applied Physics B",
        "Pressurized Irrigation Installation and Maintenance", "Pumping System Operation and Maintenance",
        "Ikinyarwanda", "English", "Applied Chemistry A",
        "Surface Drainage System Construction and Maintenance", "Entrepreneurship",
        "Practical WIR"
    ],
    "AGR": [
        "Applied Mathematics B", "Food Crops Growing and Post-Harvest Practices", "Applied Biology A",
        "Crop Protection and Extension Techniques", "Applied Physics D",
        "Horticultural and Industrial Crops Growing", "Soil Conservation",
        "Ikinyarwanda", "English", "Applied Chemistry A",
        "Farm Mechanization and Livestock Management", "Modern Farming Techniques", "Entrepreneurship",
        "Practical AGR"
    ],
    "FOP": [
        "Applied Mathematics B", "Milk products processing technology", "Applied Biology A",
        "Meat and Honey products processing technology", "Applied Physics D",
        "Fruit processing Technology", "Flour, starch and cereal processing technology",
        "Ikinyarwanda", "English", "Applied Chemistry A",
        "Cash crop and Vegetables processing technology",
        "Food microorganisms and physical-chemical properties Analysis", "Entrepreneurship",
        "Practical FOP"
    ],
    "ANH": [
        "Applied Mathematics B", "Animal Diseases Prevention and Control", "Applied Biology A",
        "Animal Diseases Diagnosis and Treatment", "Applied Physics D",
        "Anatomy, Physiology, Surgery, and Veterinary Intervention", "Ruminants, Bees, and Fish Farming Operations",
        "Ikinyarwanda", "English", "Applied Chemistry A", "Non-Ruminants Farming Operations",
        "Raw Animal Products Control and Livestock Extension", "Entrepreneurship",
        "Animal Feeding and Livestock Machinery Operations", "Practical ANH"
    ],
    "LET": [
        "Applied Mathematics B", "Shoe lasts and footwear production", "Applied Biology A",
        "Leather processing and finishing", "Applied Physics B", "Leather garments production",
        "Leather goods production", "Ikinyarwanda", "English", "Applied Chemistry A",
        "Technical drawing and pattern-making", "Leather products quality control and material quantification",
        "Entrepreneurship", "Practical LET"
    ],
    "FOR": [
        "Applied Mathematics B", "Tree Nursery Management", "Applied Biology A",
        "Forest Establishment and Protection", "Applied Physics B", "Forest Management Plan Implementation",
        "Forest Exploitation", "Ikinyarwanda", "English", "Applied Chemistry A",
        "Forests Landscape Restoration", "Entrepreneurship", "Practical FOR"
    ],
    "WOT": [
        "Applied Mathematics B", "Technical drawing, CAD, and Wooden Art style Creation",
        "Applied Biology A", "Wood properties and Timber Drying", "Applied Physics B",
        "Woodworking Machines Operation and Workshop Management", "Engineered Boards and Beams Production",
        "Ikinyarwanda", "English", "Applied Chemistry A",
        "Wooden Structures Construction", "Wooden Furniture Production", "Entrepreneurship",
        "Practical WOT"
    ],
    "FBO": [
        "Applied Mathematics C", "Food Preparation", "International Cuisines and cold kitchen Production",
        "Food and Beverage Service Quality Control", "Bakery and Pastry Products", "Food and Beverage Services",
        "Applied Professional English for Food and Beverage Operation", "Ikinyarwanda", "English",
        "Français Professionnel pour Cuisine et Service en Hôtellerie",
        "Kiswahili Mahususi Katika Huduma Za Vyakula Na Vinywaji", "Entrepreneurship",
        "Practical FBO"
    ],
    "TOR": [
        "Applied Mathematics C", "Coordinating Tour and Travel bookings", "Applied Biology A",
        "Coordinating tourism events", "Community Based Tourism and Heritage Maintenance",
        "Providing guidance on Destination", "Professional English for Tourism",
        "Ikinyarwanda", "English", "Français Professionnel pour le Tourisme",
        "Tour guiding and tour packages management", "Kutumia Kiswahili", "Entrepreneurship",
        "Practical TOR"
    ],
    "FOH": [
        "Providing Excellent Customer Services", "Housekeeping Operations", "Front Office Operations",
        "Performing Laundry Services", "Handle Hotel Guest and Luggage at Airport",
        "Professional English for Front Office", "Ikinyarwanda", "English",
        "Français Professionnel pour l'accueil et l'hébergement", "Kutumia Kiswahili", "Entrepreneurship",
        "Practical FOH"
    ],
    "MAT": [
        "Applied Mathematics B", "Metal Work", "Advanced Welding Technology",
        "Advanced Machining and Casting Technology", "Applied Physics B",
        "Mechanical machines production and Assembling Technology",
        "Installation and Maintenance of Industrial Machines and Hydropneumatic Systems",
        "Ikinyarwanda", "English", "Applied Chemistry A", "Technical Drawing and CAD Software",
        "Entrepreneurship", "Practical MAT"
    ],
    "ETE": [
        "Applied Mathematics B", "Embedded systems and artificial intelligence integration",
        "Audiovisual and broadcasting system installation", "Electronic devices repair and maintenance",
        "Applied Physics B", "Telecommunication and security systems installation",
        "Power conversion, electronic control and HVAC system installation",
        "Ikinyarwanda", "English", "Entrepreneurship", "Practical ETE"
    ],
    "ELT": [
        "Applied Mathematics B", "Industrial electrical system installation and maintenance",
        "Digital electronics and Electrical vehicle charging station installation",
        "Electrical automation and HVAC installation", "Applied Physics B",
        "Domestic electrical installation and maintenance", "Electrical power plant installation and maintenance",
        "Ikinyarwanda", "English", "Entrepreneurship", "Practical ELT"
    ],
    "REN": [
        "Applied Mathematics B", "Biomass energy and improved cooking stove production",
        "Solar energy systems installation", "Hydropower plant installation", "Applied Physics B",
        "Electrical machines installations", "Electronic Systems and EV charging station installation",
        "Ikinyarwanda", "English", "Entrepreneurship", "Practical REN"
    ],
    "BDC": [
        "Applied Mathematics B", "Construction Technical Drawing", "Reinforced Concrete Design",
        "Building elevation and Roof construction", "Applied Physics B",
        "Building materials and their applications", "Finishing works in building Construction",
        "Ikinyarwanda", "English", "Applied Chemistry A", "Entrepreneurship",
        "Practical BDC"
    ],
    "PWO": [
        "Applied Mathematics B", "Hydraulic Structures Construction", "Technical Drawing and AUTOCAD Software",
        "Pavement Layers Construction", "Applied Physics B", "Cost estimation and Masonry Works",
        "Construction Materials Testing", "Ikinyarwanda", "English",
        "Applied Chemistry A", "Road Maintenance Works", "Entrepreneurship", "Practical PWO"
    ],
    "LSV": [
        "Applied Mathematics B", "Surveying and Earthwork Computation", "Setting out of civil structures",
        "Surveying Measurements and laboratory maintenance", "Applied Physics B",
        "GIS and AutoCAD Software in mapping", "Cadastral, Mine, and Hydrographic surveying",
        "Ikinyarwanda", "English", "Applied Chemistry A", "Entrepreneurship", "Practical LSV"
    ],
    "PLT": [
        "Applied Mathematics B", "Plumbing drawing and planning", "Water supply and drainage system installation",
        "Pumping system installation", "Applied Physics B",
        "Water treatment system installation", "Water piping system",
        "Ikinyarwanda", "English", "Applied Chemistry A", "Entrepreneurship", "Practical PLT"
    ],
    "IND": [
        "Applied Mathematics B", "Soft Furnishing and Furniture design", "Interior decoration, wall and floor finishing",
        "Residential kitchen, bathroom, and partitions design", "Applied Physics B",
        "Cost estimation and interior drawing", "Exhibition stand, ceiling, doors and windows design",
        "Ikinyarwanda", "English", "Applied Chemistry A", "Entrepreneurship", "Practical IND"
    ],
    "MPA": [
        "Applied Mathematics D", "Creativity, Innovation, and Music Performance",
        "Mastering Traditional and Modern Music Performance", "Music Theory, Arrangement and Song Composition",
        "Applied Physics C", "Instrumental and Vocal Mastery in Music Performance",
        "Music Business and Industry Management", "Ikinyarwanda", "English", "Entrepreneurship",
        "Practical MPA"
    ],
    "FAD": [
        "Applied Mathematics D", "Fashion Illustration and Pattern Creation",
        "Fabric Production and Manipulation", "Sewing Techniques and Garment Construction",
        "Construction of Women's Wear and Accessories Design", "Men's Wear Styling and Marketing",
        "Ikinyarwanda", "English", "Entrepreneurship", "Practical FAD"
    ],
    "FPA": [
        "Applied Mathematics D", "Sculpture Technology", "Ceramics Technology",
        "Digital Art design and animation", "Applied Physics E",
        "Surface painting and decoration", "Artistic Drawing and Illustration",
        "Ikinyarwanda", "English", "Applied Chemistry A", "History of art and aesthetics",
        "Entrepreneurship", "Practical FPA"
    ],
    "MNT": [
        "Applied Mathematics B", "General Geology", "Fundamentals of Mine Ventilation, Safety, and Engineering Drawing",
        "Applied Chemistry C", "Mine Drilling and Blasting", "Applied Physics B",
        "Mineral Processing and Mine Rehabilitation", "Entrepreneurship",
        "Maintenance of Mining Tools and Equipment", "English", "Ikinyarwanda",
        "Practical MNT"
    ],
    "CSA": [
        "Applied Mathematics B", "Computer Power Systems and Electronic Enclosure",
        "Operating System and Data Structure with C/C++", "Cloud Infrastructure and Server Administration",
        "Integrated Computer Hardware Design, PCB Assembly, and Screen Setup", "Applied Physics B",
        "Firmware Development and Systems' Automation with PLC", "Entrepreneurship",
        "Computer System Deployment, Refurbishment and Maintenance", "English", "Ikinyarwanda",
        "Practical CSA"
    ],
    "SPE": [
        "Applied Mathematics A", "Cyber Security", "Data Structure and Algorithms",
        "Software Testing and Deployment (DevOps)", "Restful Services and Web/Web3 Application Development",
        "Cross-Platform Mobile Development", "Applied Physics A",
        "Intelligent Robotics and Embedded Systems", "Software Engineering",
        "Advanced Java Programming with OOP", "English", "Practical SPE"
    ],
    "NIT": [
        "Applied Mathematics B", "LAN and Zero Client Installation", "WAN and Fiber Optic Installation",
        "Cloud Computing", "Network and Systems Security", "Applied Physics B",
        "Network Systems Automation with Machine Learning", "Entrepreneurship",
        "IoT Systems Development and Installation", "English", "Ikinyarwanda",
        "Practical NIT"
    ],
    "SWD": [
        "Applied Mathematics B", "Front-End Design and Development", "DevOps and Software Testing",
        "Back-End Development and Database", "Applied Physics B", "System Administration",
        "Entrepreneurship", "Web3 Development and Machine Learning",
        "English", "Ikinyarwanda", "Practical SWD"
    ],
    "MMP": [
        "Applied Mathematics B", "Graphic Design", "Photography, Lighting, and Images Editing",
        "Sound Production", "Immersive Technologies and 3D Modelling", "Applied Physics C",
        "Video Production", "Entrepreneurship", "2D Animation Production",
        "Ikinyarwanda", "English", "Practical MMP"
    ]
}

reb_combinations = {
    'ACC': ['Subsidiary Accounting', 'Management Accounting', 'Entrepreneurship', 'Auditing', 'Taxation', 'Financial Accounting', 'General Studies and Communication Skills', 'English', 'Practical ACC'],
    'LFK1': ['Kiswahili', 'French', 'Entrepreneurship', 'Literature In English', 'Kinyarwanda', 'General Studies and Communication Skills', 'English'],
    'LFK2': ['French', 'Entrepreneurship', 'Literature In English', 'Kinyarwanda', 'General Studies and Communication Skills'],
    'LFK3': ['Kiswahili', 'French', 'Entrepreneurship', 'Literature In English', 'General Studies and Communication Skills'],
    'HLP': ['History', 'Psychology', 'Entrepreneurship', 'Literature In English', 'General Studies and Communication Skills', 'English'],
    'HGL': ['History', 'Entrepreneurship', 'Literature In English', 'Geography', 'General Studies and Communication Skills', 'English'],
    'PCB': ['Physics', 'Chemistry', 'Biology', 'Entrepreneurship', 'General Studies and Communication Skills'],
    'PCM': ['Physics', 'Chemistry', 'Mathematics', 'Entrepreneurship', 'General Studies and Communication Skills'],
    'MCB': ['Mathematics', 'Chemistry', 'Biology', 'Entrepreneurship', 'General Studies and Communication Skills'],
    'BCG': ['Biology', 'Chemistry', 'Geography', 'Entrepreneurship', 'General Studies and Communication Skills'],
    'MPG': ['Mathematics', 'Physics', 'Geography', 'Entrepreneurship', 'General Studies and Communication Skills'],
    'MEG': ['Mathematics', 'Economics', 'Geography', 'Entrepreneurship', 'General Studies and Communication Skills'],
    'HEG': ['History', 'Economics', 'Geography', 'Entrepreneurship', 'General Studies and Communication Skills'],
    'MPC': ['Mathematics', 'Physics', 'Computer', 'Entrepreneurship', 'General Studies and Communication Skills'],
    'LEG': ['Literature In English', 'Economics', 'Geography', 'Entrepreneurship', 'General Studies and Communication Skills'],
    'MCE': ['Mathematics', 'Economics', 'Computer', 'Entrepreneurship', 'General Studies and Communication Skills'],
    'HEL': ['History', 'Economics', 'Literature In English', 'Entrepreneurship', 'General Studies and Communication Skills'],
    'LKK': ['Kiswahili', 'Entrepreneurship', 'Kinyarwanda', 'General Studies and Communication Skills'],
    'LKF': ['Kiswahili', 'French', 'Entrepreneurship', 'Literature In English', 'General Studies and Communication Skills']
}

departments = {
    'Agricultural Engineering': [
        'Agricultural Mechanization Technology',
        'Crop Production',
        'Food Processing',
        'Horticulture Technology',
        'Irrigation and Drainage Technology'
    ],
    'Civil Engineering': [
        'Geomatics Technology',
        'Highway Technology',
        'Land Surveying',
        'Quantity Surveying',
        'Water and Sanitation Technology'
    ],
    'Creative Arts': [
        'Fashion Design',
        'Film Making and TV Production',
        'Graphic Design and Animation'
    ],
    'Electrical and Electronics Engineering': [
        'Biomedical Equipment Technology',
        'Electrical Automation Technology',
        'Electrical Technology',
        'Electromechanical Technology',
        'Electronic and Telecommunication'
    ],
    'Forestry': [
        'Forest Engineering and Wood Technology',
        'Forest Resource Management'
    ],
    'Hospitality Management': [
        'Culinary Arts',
        'Hospitality with Food and Beverage Services',
        'Hospitality with Room Division'
    ],
    'Information and Communication Technology': [
        'E-commerce',
        'Event Video',
        'Information Technology',
        'Visual Communication'
    ],
    'Mechanical Engineering': [
        'Air Conditioning and Refrigeration Technology',
        'Automobile Technology',
        'Manufacturing Technology',
        'Mechatronics Technology',
        'Renewable Energy Technology'
    ],
    'Mining Engineering': [
        'Mining Technology'
    ],
    'Nature Conservation': [
        'Wildlife and Conservation Technologies'
    ],
    'Tourism': [
        'Tourism Destination Management',
        'Tours and Travel Management'
    ],
    'Transport and Logistics': [
        'Airline and Airport Management',
        'Logistics and Supply Chain Management'
    ],
    'Veterinary Technology': [
        'Animal Health'
    ]
}

# Initialize session state
def init_session_state():
    if 'form_step' not in st.session_state:
        st.session_state.form_step = 0
    if 'current_board' not in st.session_state:
        st.session_state.current_board = None
    if 'year_completed' not in st.session_state:
        st.session_state.year_completed = None
    if 'selected_combination' not in st.session_state:
        st.session_state.selected_combination = None
    if 'subject_marks' not in st.session_state:
        st.session_state.subject_marks = {}
    if 'rp_admission_year' not in st.session_state:
        st.session_state.rp_admission_year = None
    if 'department' not in st.session_state:
        st.session_state.department = None
    if 'course' not in st.session_state:
        st.session_state.course = None
    if 'year_study' not in st.session_state:
        st.session_state.year_study = None
    if 'confirm_delete' not in st.session_state:
        st.session_state.confirm_delete = False

# File paths
JSON_FILE = "rp_student_data.json"
CSV_FILE = "rp_student_data.csv"

# Load existing data
def load_existing_data():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_data(new_data):
    # Load existing data
    existing_data = load_existing_data()
    
    # Append new data
    updated_data = existing_data + new_data
    
    # Save to JSON
    try:
        with open(JSON_FILE, 'w') as f:
            json.dump(updated_data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving JSON file: {e}")
        return existing_data
    
    # Save to CSV
    if updated_data:
        try:
            df = pd.DataFrame(updated_data)
            
            # Flatten the marks column for CSV
            if not df.empty and 'marks' in df.columns:
                marks_df = pd.json_normalize(df['marks'])
                marks_df.columns = [f'mark_{col}' for col in marks_df.columns]
                df = df.drop('marks', axis=1).join(marks_df)
            
            df.to_csv(CSV_FILE, index=False)
        except Exception as e:
            st.error(f"Error saving CSV file: {e}")
    
    return updated_data

def reset_form():
    """Reset all form state"""
    st.session_state.form_step = 0
    st.session_state.current_board = None
    st.session_state.year_completed = None
    st.session_state.selected_combination = None
    st.session_state.subject_marks = {}
    st.session_state.rp_admission_year = None
    st.session_state.department = None
    st.session_state.course = None
    st.session_state.year_study = None
    st.session_state.confirm_delete = False

def main():
    # Initialize session state
    init_session_state()
    
    # Initialize years
    current_year = datetime.now().year
    high_school_years = list(range(current_year, current_year - 6, -1))
    rp_admission_years = list(range(current_year, current_year - 2, -1))

    # App layout
    st.set_page_config(page_title="RP Student Performance Data Collection", layout="wide")

    # Header with CSS
    st.markdown("""
        <style>
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .step-indicator {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }
        .board-option {
            padding: 20px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .board-option.selected {
            border-color: #667eea;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        }
        .subject-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .progress-bar {
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            height: 10px;
            margin-bottom: 20px;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="header">
            <h1>RP Student Research Data Collection</h1>
            <p>Rwanda Student Performance Analysis - RTB & REB High School Scores</p>
        </div>
    """, unsafe_allow_html=True)

    # Progress indicator
    progress_steps = [
        "Select Board",
        "Year Completed", 
        "Combination", 
        "Subject Marks", 
        "RP Admission Year", 
        "Department", 
        "Course", 
        "Year of Study"
    ]

    current_step = min(st.session_state.form_step, len(progress_steps) - 1)
    progress_percentage = (current_step + 1) / len(progress_steps) * 100

    st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress_percentage}%"></div>
        </div>
        <div class="step-indicator">
            <strong>Step {current_step + 1} of {len(progress_steps)}: {progress_steps[current_step]}</strong>
        </div>
    """, unsafe_allow_html=True)

    # Step 1: Board selection
    if st.session_state.form_step == 0:
        st.subheader("Select High School Examination Board")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div style="text-align: center; padding: 20px; border: 2px solid #e1e5e9; border-radius: 10px; margin-bottom: 10px;">
                    <h3>RTB (TSS)</h3>
                    <p>Rwanda TVET Board</p>
                    <p><small>(Technical & Vocational)</small></p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Select RTB", key="rtb_btn", use_container_width=True):
                st.session_state.current_board = "RTB"
                st.session_state.form_step = 1
                st.rerun()
        
        with col2:
            st.markdown("""
                <div style="text-align: center; padding: 20px; border: 2px solid #e1e5e9; border-radius: 10px; margin-bottom: 10px;">
                    <h3>REB</h3>
                    <p>Rwanda Education Board</p>
                    <p><small>(Academic Preparation)</small></p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Select REB", key="reb_btn", use_container_width=True):
                st.session_state.current_board = "REB"
                st.session_state.form_step = 1
                st.rerun()

    # Step 2: Year Completed
    elif st.session_state.form_step == 1:
        st.info(f"Selected Board: **{st.session_state.current_board}**")
        
        st.subheader("Year of Completing High School")
        year_completed = st.selectbox(
            "Select year:",
            options=[None] + high_school_years,
            format_func=lambda x: "Select year..." if x is None else str(x),
            index=0
        )
        
        if year_completed:
            st.session_state.year_completed = year_completed
            if st.button("Next Step", type="primary"):
                st.session_state.form_step = 2
                st.rerun()

    # Step 3: Combination Selection
    elif st.session_state.form_step == 2:
        st.info(f"Board: **{st.session_state.current_board}** | Year Completed: **{st.session_state.year_completed}**")
        
        st.subheader("Select Combination")
        combinations = rtb_combinations if st.session_state.current_board == "RTB" else reb_combinations

        combo_options = []
        
        if st.session_state.current_board == "RTB":
            # RTB combinations with short + full form
            rtb_full_names = {
                "AUT": "Automobile Technology",
                "WIR": "Water and Irrigation",
                "AGR": "Agriculture",
                "FOP": "Food Processing",
                "ANH": "Animal Health",
                "LET": "Leather Technology",
                "FOR": "Forestry",
                "WOT": "Wood Technology",
                "FBO": "Food and Beverage Operations",
                "TOR": "Tourism",
                "FOH": "Front Office and Housekeeping",
                "MAT": "Manufacturing Technology",
                "ETE": "Electronics and Telecommunication",
                "ELT": "Electrical Technology",
                "REN": "Renewable Energy",
                "BDC": "Building Construction",
                "PWO": "Public Works",
                "LSV": "Land Surveying",
                "PLT": "Plumbing Technology",
                "IND": "Interior Design",
                "MPA": "Music and Performing Arts",
                "FAD": "Fashion Design",
                "FPA": "Fine and Plastic Arts",
                "MNT": "Mining Technology",
                "CSA": "Computer System and Architecture",
                "SPE": "Software Programming and Embedded Systems",
                "NIT": "Networking and Internet Technology",
                "SWD": "Software Development",
                "MMP": "Multimedia Production"
            }

            for combo in combinations.keys():
                full_name = rtb_full_names.get(combo, "")
                combo_options.append(f"{combo} - {full_name}")

        else:
            # REB combinations with short + full words
            reb_full_names = {
                "ACC": "Accounting",
                "LFK1": "Literature in English – French – Kinyarwanda – Kiswahili",
                "LFK2": "Literature in English – French – Kinyarwanda",
                "LFK3": "Literature in English – Kiswahili – French",
                "HLP": "History – Literature in English – Psychology",
                "HGL": "History – Geography – Literature in English",
                "PCB": "Physics – Chemistry – Biology",
                "PCM": "Physics – Chemistry – Mathematics",
                "MCB": "Mathematics – Chemistry – Biology",
                "BCG": "Biology – Chemistry – Geography",
                "MPG": "Mathematics – Physics – Geography",
                "MEG": "Mathematics – Economics – Geography",
                "HEG": "History – Economics – Geography",
                "MPC": "Mathematics – Physics – Computer Science",
                "LEG": "Literature in English – Economics – Geography",
                "MCE": "Mathematics – Computer Science – Economics",
                "HEL": "History – Economics – Literature in English",
                "LKK": "Literature in English – Kiswahili – Kinyarwanda",
                "LKF": "Literature in English – Kiswahili – French"
            }

            for code, full_name in reb_full_names.items():
                combo_options.append(f"{code} - {full_name}")

        # Select box
        selected_combo_display = st.selectbox(
            "Choose a combination:",
            options=[None] + combo_options,
            format_func=lambda x: "Choose a combination..." if x is None else x,
            index=0
        )

        if selected_combo_display:
            # Extract only the code before " - "
            selected_combination = selected_combo_display.split(" - ")[0]
            st.session_state.selected_combination = selected_combination
            
            if st.button("Next Step", type="primary"):
                st.session_state.form_step = 3
                st.rerun()

    # Step 4: Subject Marks
    elif st.session_state.form_step == 3:
        st.info(f"Board: **{st.session_state.current_board}** | Year: **{st.session_state.year_completed}** | Combination: **{st.session_state.selected_combination}**")
        
        st.subheader("Enter Marks Obtained in National Examination for Each Subject (1-100)")
        combinations = rtb_combinations if st.session_state.current_board == "RTB" else reb_combinations
        subjects = combinations[st.session_state.selected_combination]
        
        # Initialize marks if not exists
        if not st.session_state.subject_marks:
            st.session_state.subject_marks = {subject: "" for subject in subjects}
        
        # Create input fields in columns
        cols = st.columns(2)
        all_marks_entered = True
        invalid_marks = False
        
        for i, subject in enumerate(subjects):
            with cols[i % 2]:
                # Use number input with proper validation
                current_value = st.session_state.subject_marks.get(subject, "")
                if current_value == "":
                    current_value = None
                elif isinstance(current_value, str) and current_value.isdigit():
                    current_value = int(current_value)
                
                mark = st.number_input(
                    subject,
                    min_value=1,
                    max_value=100,
                    value=current_value,
                    step=1,
                    key=f"mark_{subject}_{st.session_state.form_step}",
                    help="Enter a number between 1 and 100"
                )
                
                if mark is not None:
                    st.session_state.subject_marks[subject] = mark
                else:
                    st.session_state.subject_marks[subject] = ""
                    all_marks_entered = False
        
        if all_marks_entered and not invalid_marks:
            if st.button("Next Step", type="primary"):
                st.session_state.form_step = 4
                st.rerun()
        else:
            if not all_marks_entered:
                st.warning("Please enter marks for all subjects to proceed to the next step")

    # Step 5: RP Admission Year
    elif st.session_state.form_step == 4:
        st.info(f"Board: **{st.session_state.current_board}** | Combination: **{st.session_state.selected_combination}** | Subjects completed ✓")
        
        st.subheader("Year of Admission to RP")
        rp_admission_year = st.selectbox(
            "Select year:",
            options=[None] + rp_admission_years,
            format_func=lambda x: "Select year..." if x is None else str(x),
            index=0
        )
        
        if rp_admission_year:
            st.session_state.rp_admission_year = rp_admission_year
            if st.button("Next Step", type="primary"):
                st.session_state.form_step = 5
                st.rerun()

    # Step 6: Department Selection
    elif st.session_state.form_step == 5:
        st.info(f"Board: **{st.session_state.current_board}** | RP Admission: **{st.session_state.rp_admission_year}**")
        
        st.subheader("Select Department")
        department = st.selectbox(
            "Choose a department:",
            options=[None] + list(departments.keys()),
            format_func=lambda x: "Choose a department..." if x is None else x,
            index=0
        )
        
        if department:
            st.session_state.department = department
            if st.button("Next Step", type="primary"):
                st.session_state.form_step = 6
                st.rerun()

    # Step 7: Course Selection
    elif st.session_state.form_step == 6:
        st.info(f"Department: **{st.session_state.department}**")
        
        st.subheader("Select Course/Program")
        course = st.selectbox(
            "Choose a course:",
            options=[None] + departments[st.session_state.department],
            format_func=lambda x: "Choose a course..." if x is None else x,
            index=0
        )
        
        if course:
            st.session_state.course = course
            if st.button("Next Step", type="primary"):
                st.session_state.form_step = 7
                st.rerun()

    # Step 8: Year of Study
    elif st.session_state.form_step == 7:
        st.info(f"Department: **{st.session_state.department}** | Course: **{st.session_state.course}**")
        
        st.subheader("Current Year of Study")
        year_study = st.selectbox(
            "Select year:",
            options=[None, "Year 1", "Year 2"],
            format_func=lambda x: "Select year..." if x is None else x,
            index=0
        )
        
        if year_study:
            st.session_state.year_study = year_study
            
            # Show summary and submit
            st.subheader("Review Your Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Basic Information:**")
                st.write(f"- Board: {st.session_state.current_board}")
                st.write(f"- Year Completed HS: {st.session_state.year_completed}")
                st.write(f"- Combination: {st.session_state.selected_combination}")
                st.write(f"- RP Admission Year: {st.session_state.rp_admission_year}")
                st.write(f"- Year of Study: {st.session_state.year_study}")
            
            with col2:
                st.write("**Academic Information:**")
                st.write(f"- Department: {st.session_state.department}")
                st.write(f"- Course: {st.session_state.course}")
                
                st.write("**Subject Marks:**")
                for subject, mark in st.session_state.subject_marks.items():
                    st.write(f"- {subject}: {mark}")
            
            if st.button("Submit Student Data", type="primary"):
                # Create data record
                form_data = {
                    "id": datetime.now().timestamp(),
                    "timestamp": datetime.now().isoformat(),
                    "examinationBoard": st.session_state.current_board,
                    "yearCompleted": st.session_state.year_completed,
                    "rpAdmissionYear": st.session_state.rp_admission_year,
                    "combination": st.session_state.selected_combination,
                    "department": st.session_state.department,
                    "course": st.session_state.course,
                    "yearStudy": st.session_state.year_study,
                    "marks": st.session_state.subject_marks
                }
                
                # Save data
                updated_data = save_data([form_data])
                
                # Move to success step
                st.session_state.form_step = 8
                st.rerun()

    # Step 9: Success and Summary
    elif st.session_state.form_step == 8:
        st.markdown("""
            <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; border-radius: 15px; margin-bottom: 30px;">
                <h1>🎉 Congratulations!</h1>
                <h2>Student data submitted successfully!</h2>
                <p style="font-size: 1.2em; margin-top: 20px;">
                    Your data has been saved confidentially and is now part of our research database.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Data Collection Summary
        st.subheader("Data Collection Summary")
        
        # Load and display data count
        existing_data = load_existing_data()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Students Recorded", len(existing_data))
        
        # Download buttons
        st.subheader("Download Data")
        
        download_col1, download_col2 = st.columns(2)
        
        with download_col1:
            if os.path.exists(JSON_FILE):
                with open(JSON_FILE, "r") as f:
                    st.download_button(
                        label="Download JSON",
                        data=f.read(),
                        file_name=f"rp_student_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True,
                        disabled=True
                    )

        with download_col2:
            if os.path.exists(CSV_FILE):
                with open(CSV_FILE, "r") as f:
                    st.download_button(
                        label="Download CSV",
                        data=f.read(),
                        file_name=f"rp_student_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        disabled=True
                    )
        
        # Additional options
        st.markdown("---")
        
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("Add Another Student", type="primary", use_container_width=True):
                reset_form()
                st.rerun()
        
        with action_col2:
            if st.button("View All Data", use_container_width=True,disabled=True):
                # Show data table
                st.subheader("All Recorded Data")
                df = pd.DataFrame(existing_data)
                
                # Flatten marks for display
                if not df.empty and 'marks' in df.columns:
                    marks_df = pd.json_normalize(df['marks'])
                    marks_df.columns = [f'mark_{col}' for col in marks_df.columns]
                    df_display = df.drop('marks', axis=1).reset_index(drop=True)
                    df_display = pd.concat([df_display, marks_df], axis=1)
                else:
                    df_display = df
                
                st.dataframe(df_display, use_container_width=True)

        with action_col3:
            if st.button("Clear All Data", use_container_width=True,disabled=True):
                if st.session_state.get('confirm_delete', False):
                    try:
                        if os.path.exists(JSON_FILE):
                            os.remove(JSON_FILE)
                        if os.path.exists(CSV_FILE):
                            os.remove(CSV_FILE)
                        st.success("All data has been cleared!")
                        st.session_state.confirm_delete = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error clearing data: {e}")
                else:
                    st.session_state.confirm_delete = True
                    st.warning("Click again to confirm deletion of all data")
                    st.rerun()

    # Navigation buttons
    if st.session_state.form_step > 0 and st.session_state.form_step < 8:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("Previous Step"):
                st.session_state.form_step -= 1
                st.rerun()
        
        with col2:
            if st.button("Reset Form"):
                if st.button("Confirm Reset", key="confirm_reset"):
                    reset_form()
                    st.rerun()
                else:
                    st.warning("Click 'Confirm Reset' to reset the form")

    # Show initial summary only if no form is in progress
    # if st.session_state.form_step == 0:
    #     st.markdown("---")
    #     st.subheader("Data Collection Overview")
        
    #     # Load and display data count
    #     existing_data = load_existing_data()
        
        # if existing_data:
        #     st.metric("Total Students Recorded", len(existing_data))
            
        #     if st.button("View Existing Data", disabled=True):
        #         df = pd.DataFrame(existing_data)
                
        #         # Flatten marks for display
        #         if not df.empty and 'marks' in df.columns:
        #             marks_df = pd.json_normalize(df['marks'])
        #             marks_df.columns = [f'mark_{col}' for col in marks_df.columns]
        #             df_display = df.drop('marks', axis=1).reset_index(drop=True)
        #             df_display = pd.concat([df_display, marks_df], axis=1)
        #         else:
        #             df_display = df
                
        #         st.dataframe(df_display.head(5), use_container_width=True)
        #         st.caption("Showing first 5 records. Complete the form to access full data management.")
        # else:
        #     st.info("No data has been collected yet. Start by selecting an examination board above.")

if __name__ == "__main__":
    main()
