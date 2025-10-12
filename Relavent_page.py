from streamlit import streamlit as st

def show_compare_page():
    """Display the comparison page content"""
    st.title("Compare Sequences")
    st.write("This page can be used to compare analysis results of different sequences.")

    # Add comparison functionality code here
    st.info("Comparison feature is under development. Stay tuned!")


def show_help_page():
    """Display the help page content"""
    st.title("Help & Documentation")
    st.write("Welcome to the NCyclase prediction tool help page.")

    with st.expander("What is the AC/GC prediction tool?", expanded=True):
        st.write("""
        AC/GC-Pred is a tool for predicting functional centers of adenylate cyclase (AC) 
        and guanylate cyclase (GC) in protein sequences. These enzymes play key roles 
        in cellular signal transduction.
        """)

    with st.expander("How to use the tool?"):
        st.write("""
        1. Select analysis type (AC-Pred or GC-Pred) on the home page
        2. Enter protein sequences in FASTA format or upload sequence files
        3. Click the "Analyze" button
        4. View analysis results and visualizations
        """)

    with st.expander("How to interpret results?"):
        st.write("""
        - Red region (<0.3): Low confidence
        - Orange region (0.3-0.7): Medium confidence
        - Green region (>0.7): High confidence

        Recommended matches should have:
        - Two or more green physicochemical values (GH, GW, GP)
        - Green overall G-value
        - No red values
        """)


def show_export_page():
    """Display the export page content"""
    st.title("Export Results")
    st.write("This page allows you to export and save analysis results.")

    # Add export options
    st.subheader("Select Export Format")
    export_format = st.radio(
        "Export format:",
        ["CSV", "Excel", "JSON", "PDF Report"]
    )

    st.subheader("Select Export Content")
    export_options = st.multiselect(
        "Export content:",
        ["Sequence Panel", "Detailed scores", "hit_table", "Charts"]
    )

    st.button("Export Data")

    st.info("Please complete sequence analysis on the home page before using export features.")


def show_about_page():
    """Display the about page content"""
    st.title("About AC/GC-Pred")

    st.write("""
    ## Project Introduction

    AC/GC-Pred is a tool for predicting functional centers of adenylate cyclase (AC) 
    and guanylate cyclase (GC) in protein sequences. These enzymes play important roles 
    in cellular signal transduction, participating in various physiological and pathological processes.

    ## Technical Implementation

    This tool uses machine learning and sequence analysis techniques to identify potential 
    functional centers based on specific amino acid patterns and physicochemical properties.

    ## Research Team

    []

    ## Contact Information

    Email: zhangga@kean.edu.cn

    ## Citation

     cite:

    [Citation information]
    """)


def show_publications_page():
    """Display the publications page content"""
    st.title("Publications")

    st.write("""
    ## Related Papers

    List of research papers related to AC/GC-Pred:
    """)

    # Display papers list
    papers = [
        {
            "title": "",
            "authors": "",
            "journal": "",
            "year": "",
            "doi": ""
        }

    ]

    for i, paper in enumerate(papers, 1):
        st.markdown(f"""
        ### {i}. {paper['title']}

        **Authors**: {paper['authors']}  
        **Journal**: {paper['journal']}  
        **Year**: {paper['year']}  
        **DOI**: {paper['doi']}

        ---
        """)


def show_contact_page():
    """Display the contact page content"""
    st.title("Contact Us")

    st.write("""
    If you have any questions, suggestions, or collaboration interests, please feel free to contact us.
    """)

    # Create contact form
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        institution = st.text_input("Institution/Organization")
        message_type = st.selectbox(
            "Message type",
            ["Question", "Bug report", "Feature suggestion", "Collaboration interest", "Other"]
        )
        message = st.text_area("Message content")

        submit_button = st.form_submit_button("Send Message")

        if submit_button:
            st.success("Your message has been sent! We will respond as soon as possible.")

    st.write("""
    ## Contact Information

    **Email**: zhangga@kean.edu.cn

    **Address**: 
    Wenzhou-Kean University 
    88 Daxue Rd, Wenzhou, Ouhai, Zhejiang, China 325060

    **Phone**: 15988336903
    """)