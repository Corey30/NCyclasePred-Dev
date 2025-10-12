import base64
import os

import streamlit as st
import pandas as pd


from Relavent_page import show_compare_page, show_help_page, show_export_page, show_about_page, \
    show_publications_page, show_contact_page
from motify_finder import find_ac_hits, find_gc_hits, generate_hit_markers
from read_fasta_input import read_fasta_input
from Protein_Database import AMINO_ACID_PROPERTIES
from visualization import plot_weighted_properties, generate_sequence_panel_html, plot_hit_distribution
from ui_components import create_results_table


def get_image_base64(image_path):
    """获取图片的base64编码"""
    if not os.path.isfile(image_path):
        return None

    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Main Streamlit app

def show_home_page():
  pass


def main():
    st.set_page_config(page_title="AC/GC Prediction Tool",
                       page_icon="",
                       layout="wide"
                       )

    # 初始化页面状态 - 添加这一行
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    # 尝试加载背景图片
    img_base64 = get_image_base64("banner_background.jpg")

    if img_base64:
        # 使用图片作为背景
        background_style = f"""
            .title-container {{
                background-image: url('data:image/jpeg;base64,{img_base64}');
                background-size: cover;
                background-position: center;
                padding: 30px;
                border-radius: 5px;
                margin-bottom: 20px;
                text-align: center;
            }}
            """
    else:
        # 使用渐变色作为备用
        background_style = """
            .title-container {
                background-image: linear-gradient(to right, #8B0000, #FF6B6B);
                background-size: cover;
                background-position: center;
                padding: 30px;
                border-radius: 5px;
                margin-bottom: 20px;
                text-align: center;
            }
            """

    # 添加样式
    st.markdown(f"""
        <style>
        {background_style}
        .title-text {{
            color: white;
            font-size: 2.5rem;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            margin-bottom: 5px;
        }}
        .subtitle-text {{
            color: white;
            font-size: 1.2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }}
        </style>
        """, unsafe_allow_html=True)

    # 添加带背景的标题
    st.markdown("""
        <div class="title-container">
            <div class="title-text">NCyclase prediction tool</div>
            <div class="subtitle-text">Powered by AC/GC-Pred</div>
        </div>
        """, unsafe_allow_html=True)

    # 创建导航按钮并处理页面切换
    cols = st.columns(7)

    # 定义页面切换回调函数
    def navigate_to(page_name):
        st.session_state.page = page_name
        # 如果有其他状态需要重置，可以在这里添加

    

    # 创建导航按钮
    with cols[0]:
        if st.button("Home", key="nav_home", on_click=navigate_to, args=('home',)):
            pass
    with cols[1]:
        if st.button("Compare", key="nav_compare", on_click=navigate_to, args=('compare',)):
            pass
    with cols[2]:
        if st.button("Help", key="nav_help", on_click=navigate_to, args=('help',)):
            pass
    with cols[3]:
        if st.button("Export", key="nav_export", on_click=navigate_to, args=('export',)):
            pass
    with cols[4]:
        if st.button("About", key="nav_about", on_click=navigate_to, args=('about',)):
            pass
    with cols[5]:
        if st.button("Publications", key="nav_publications", on_click=navigate_to, args=('publications',)):
            pass
    with cols[6]:
        if st.button("Contact", key="nav_contact", on_click=navigate_to, args=('contact',)):
            pass



    st.markdown("<hr>", unsafe_allow_html=True)
    if st.session_state.page=='home':
        show_home_page()
    elif st.session_state.page == 'compare':
        show_compare_page()
    elif st.session_state.page == 'help':
        show_help_page()
    elif st.session_state.page == 'export':
        show_export_page()
    elif st.session_state.page == 'about':
        show_about_page()
    elif st.session_state.page == 'publications':
        show_publications_page()
    elif st.session_state.page == 'contact':
        show_contact_page()


    # Sidebar
    st.sidebar.title("Navigation: AC/GC prediction tool and Input form for you to choose")
    st.sidebar.markdown("---")

    with st.sidebar.expander("Analysis Type", expanded=True):
        analysis_type = st.radio(
            "Select analysis tool:",
            ["AC-Pred", "GC-Pred"]
        )

    with st.sidebar.expander("Sequence Input", expanded=True):
        input_method = st.radio(
            "Select input form:",
            ["Paste Sequence", "Upload File"]
        )

    with st.sidebar.expander("Advanced Options", expanded=False):
        threshold = st.slider("Score Threshold", 0.0, 1.0, 0.3)
        highlight_hits = st.checkbox("Highlight matches", value=True)
        show_details = st.checkbox("Show detailed scores", value=True)
        window_size = st.slider("Window Size for Property Profiles", 3, 15, 5)
    # 在侧边栏的各个组件之后添加一个空白区域，让logo显示在底部
    st.sidebar.markdown("<br>" * 3, unsafe_allow_html=True)

    # 添加Logo和版权信息到侧边栏底部
    st.sidebar.markdown("---")
    st.sidebar.image("wenzhou_kean_logo.png", width=200)
    st.sidebar.markdown("<p style='text-align: center; font-size: 12px;'>WENZHOU-KEAN UNIVERSITY</p>",
                        unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center; font-size: 10px; color: gray;'>© 2025 All Rights Reserved.</p>",
                        unsafe_allow_html=True)

    # Session state management
    if 'sequences' not in st.session_state:
        st.session_state.sequences = {}
    if 'ac_results' not in st.session_state:
        st.session_state.ac_results = {}
    if 'gc_results' not in st.session_state:
        st.session_state.gc_results = {}
    if 'analysis_type' not in st.session_state:
        st.session_state.analysis_type = analysis_type
    if 'current_view' not in st.session_state:
        st.session_state.current_view = "input"

    st.session_state.analysis_type = analysis_type

    if st.session_state.current_view == "input":
        render_input_page(analysis_type, input_method)
    elif st.session_state.current_view == "results":
        render_results_page(analysis_type)


def render_input_page(analysis_type, input_method):
    # 第一行：预测部分
    st.subheader("Prediction:")
    st.markdown(f"**Analysis Type:** {analysis_type}")

    if analysis_type == "AC-Pred":
        st.markdown("""
        **AC Motif Pattern:** 
        [KS]X[DE]X(10)[KR]X(0,2)[DE]
        """)
    else:
        st.markdown("""
        **GC Motif Pattern:**
        [KS]X[SCG]X(10)[KR]X(0,2)[DE]
        """)

    # 第二行：序列输入部分
    st.subheader("Sequence Input")

    if input_method == "Paste Sequence":
        sequence_input = st.text_area(
            "Enter FASTA sequence(s):",
            height=350,
            placeholder=">Sequence_name\nMKLSTAVLLALLVLQAASYGRPLGDAVRAPR...",
            help="Enter one or more protein sequences in FASTA format"
        )

        if st.button("Analyze Sequences", key=f"analyze_{analysis_type.lower()}"):
            if sequence_input:
                try:
                    with st.spinner("Processing sequences..."):
                        process_sequences(sequence_input, analysis_type)
                        st.session_state.current_view = "results"
                        st.rerun()
                except Exception as e:
                    st.error(f"Error processing sequences: {str(e)}")
            else:
                st.warning("Your input can't be empty, please enter FASTA formatted sequences.")
    else:
        uploaded_file = st.file_uploader(
            f"Upload FASTA file for {analysis_type} analysis:",
            type=["fasta", "fa", "txt"]
        )

        if uploaded_file is not None:
            sequence_input = uploaded_file.getvalue().decode("utf-8")
            st.success(f"File '{uploaded_file.name}' uploaded successfully.")
            st.text_area("Preview:", sequence_input[:500] + ("..." if len(sequence_input) > 500 else ""),
                         height=150)

            if st.button("Analyze File", key=f"analyze_file_{analysis_type.lower()}"):
                try:
                    with st.spinner("Processing sequences..."):
                        process_sequences(sequence_input, analysis_type)
                        st.session_state.current_view = "results"
                        st.rerun()
                except Exception as e:
                    st.error(f"Error processing sequences: {str(e)}")

    # 输入示例部分（可选，根据您的需求可以保留或删除）
    st.markdown("**Input Example:**")
    st.text_area(
        "",
        value=">sp|Q9ERL9|GCYA1_MOUSE Guanylate cyclase soluble subunit alpha-1 OS=Mus musculus OX=10090 GN=Gucy1a1 PE=1 SV=2\nMFCRKFKDLKITGECPFSLLAPGQVPKEPTEEVAGGSEGCQATLPICQYFPEKNAEGSLP",
        height=150,
        disabled=True
    )


def process_sequences(sequence_input, analysis_type):
    st.session_state.sequences = read_fasta_input(sequence_input)
    if analysis_type == "AC-Pred":
        st.session_state.ac_results = find_ac_hits(st.session_state.sequences)
    else:
        st.session_state.gc_results = find_gc_hits(st.session_state.sequences)


def render_sequence_panel(selected_sequence, sequence_data, results, analysis_type):
    """
    Render the sequence panel with highlighted motif matches

    Args:
        selected_sequence (str): Name of the selected sequence
        sequence_data (str): The full sequence string
        results (dict): Dictionary with matched results
        analysis_type (str): Type of analysis (AC-Pred or GC-Pred)
    """
    st.subheader("Sequence Panel View")

    if selected_sequence in results:
        hits = results[selected_sequence]
        sequence = sequence_data

        # Generate hit markers for visualization
        hit_markers = generate_hit_markers(sequence, hits)

        # Create sequence panel with highlighted matches
        sequence_html = generate_sequence_panel_html(sequence, hit_markers)
        st.markdown(sequence_html, unsafe_allow_html=True)

        # Add hit distribution visualization
        st.subheader("")
        fig = plot_hit_distribution(sequence, hit_markers)
        st.pyplot(fig)

        # Add help text
        with st.expander("Sequence Panel View Help", expanded=False):
            st.markdown("""
            **Color Key:**
            - **Light Red Background**: Single motif match
            - **Yellow Background**: Overlapping motif matches (higher confidence)

            The sequence is displayed with 1-based numbering. The "Motif Match Distribution" 
            shows the density of matches across the sequence, with darker colors indicating 
            more overlapping matches at that position.
            """)
    else:
        st.info(f"No {analysis_type} matches found for {selected_sequence}")


def render_results_page(analysis_type):
    import matplotlib.pyplot as plt
    import math
    import base64

    if st.button("← Back to Input", key="back_to_input"):
        st.session_state.current_view = "input"
        st.rerun()

    results = st.session_state.ac_results if analysis_type == "AC-Pred" else st.session_state.gc_results

    if not results:
        st.warning(f"No {analysis_type} matches found in processed sequences.")
        st.info("Potential reasons:")
        if analysis_type == "AC-Pred":
            st.info("- No regions matching [KS]X[DE]X(10)[KR]X(0,2)[DE] pattern")
        else:
            st.info("- No regions matching [KS]X[SCG]X(10)[KR]X(0,2)[DE] pattern")
        st.info("- Check your sequences or try different analysis type")
        return

    st.subheader("Hit Table")


    results_df = create_results_table(results)
    st.markdown(results_df.to_html(escape=False, index=False), unsafe_allow_html=True)#use html to show the table

    # add CSS style to show right color
    st.markdown("""
    <style>
        td span {
            display: inline-block;
            padding: 2px 5px;
            border-radius: 3px;
            font-weight: bold;
        }
        td span[style*="color:red"] {
            background-color: #ffcccc;
            color: black !important;
        }
        td span[style*="color:orange"] {
            background-color: #fff2cc;
            color: black !important;
        }
        td span[style*="color:green"] {
            background-color: #ccffcc;
            color: black !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # csv download
    export_rows = []
    for seq_name, hits in results.items():
        for position, hit_data in hits.items():
            properties = hit_data["properties"]
            weighted_props = hit_data["weighted_properties"]

            export_rows.append({
                "Sequence Name": seq_name,
                "Position": position,
                "Matched Sequence": hit_data["amino_acid_sequence"],
                "Avg Hydrophobicity": properties['average_hydrophobicity'],
                "Avg MW": properties['average_molecular_weight'],
                "Avg pI": properties['average_isoelectric_point'],
                "GH Score": weighted_props['GH'],
                "GW Score": weighted_props['GW'],
                "GP Score": weighted_props['GP'],
                "G Overall": weighted_props['G']
            })

    export_df = pd.DataFrame(export_rows)


    csv = export_df.to_csv(index=False)
    csv_data = base64.b64encode(csv.encode()).decode()

    st.download_button(
        label="Download as CSV",
        data=csv_data,
        file_name=f"{analysis_type.lower()}_hit_table.csv",
        mime="text/csv"
    )

    st.markdown("---")

    col1, col2 = st.columns([1, 4])

    with col1:
        st.subheader("")
        sequence_options = list(results.keys())
        if not sequence_options:
            st.info("No results to display.")
            return

        selected_sequence = st.selectbox("Select Matched Sequence:", sequence_options, key="select_sequence_main")

        if selected_sequence:
            position_options = list(results[selected_sequence].keys())
            if not position_options:
                st.info(f"No matches found in {selected_sequence}.")
                return

            selected_position = st.selectbox("Select Match Position:", position_options, key="select_position_main")

            if selected_position:
                hit_data = results[selected_sequence][selected_position]

                st.markdown(f"**Sequence:** {selected_sequence}")
                st.markdown(f"**Position:** {selected_position}")
                st.markdown(f"**Cyclase Sequence:** `{hit_data['amino_acid_sequence']}`")
                st.markdown(f"**Sequence Length:** {len(hit_data['amino_acid_sequence'])}")

                weighted_props = hit_data["weighted_properties"]
                for prop, value in weighted_props.items():
                    color = "red"
                    if value > 0.7:
                        color = "green"
                    elif value > 0.3:
                        color = "orange"
                    st.markdown(f"**{prop}:** <span style='color:{color};'>{value:.3f}</span>", unsafe_allow_html=True)

    with col2:
        if not selected_sequence:
            st.info("Select a sequence to view details.")
            return

        full_sequence = st.session_state.sequences[selected_sequence]
        render_sequence_panel(selected_sequence, full_sequence, results, analysis_type)

        if selected_position:
            hit_data = results[selected_sequence][selected_position]

            st.markdown("---")
            st.subheader("Analysis Charts")
            tabs = st.tabs(["Property Analysis", "Score Distribution", "Confidence Analysis"])

            with tabs[0]:
                window_size = st.session_state.get('window_size', 6)

                # Get property data for all positions
                property_data = []
                for i, aa in enumerate(hit_data['amino_acid_sequence']):
                    if aa in AMINO_ACID_PROPERTIES:
                        property_data.append({
                            'Position': i + 1,
                            'Hydrophobicity': AMINO_ACID_PROPERTIES[aa]['hydrophobicity'],
                            'Molecular Weight': AMINO_ACID_PROPERTIES[aa]['molecular_weight'] / 100,
                            'Isoelectric Point': AMINO_ACID_PROPERTIES[aa]['isoelectric_point']
                        })
                    else:
                        property_data.append({
                            'Position': i + 1,
                            'Hydrophobicity': 0,
                            'Molecular Weight': 0,
                            'Isoelectric Point': 0
                        })

                property_df = pd.DataFrame(property_data)

                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(property_df['Position'], property_df['Hydrophobicity'], 'b-', label='Hydrophobicity')
                ax.plot(property_df['Position'], property_df['Molecular Weight'], 'r-', label='MW (scaled)')
                ax.plot(property_df['Position'], property_df['Isoelectric Point'], 'g-', label='pI')

                key_positions = []
                if analysis_type == "AC-Pred":
                    key_positions = [1, 3]
                    # Find KR position
                    seq = hit_data['amino_acid_sequence']
                    for i in range(13, len(seq) - 1):
                        if seq[i] in ('K', 'R'):
                            key_positions.append(i + 1)
                            break
                    # Find DE position at the end
                    for i in range(len(seq) - 1, -1, -1):
                        if seq[i] in ('D', 'E'):
                            key_positions.append(i + 1)
                            break
                else:
                    key_positions = [1, 3]
                    # Find KR position
                    seq = hit_data['amino_acid_sequence']
                    for i in range(13, len(seq) - 1):
                        if seq[i] in ('K', 'R'):
                            key_positions.append(i + 1)
                            break
                    # Find DE position at the end
                    for i in range(len(seq) - 1, -1, -1):
                        if seq[i] in ('D', 'E'):
                            key_positions.append(i + 1)
                            break

                for pos in key_positions:
                    ax.axvline(x=pos, color='gray', linestyle='--', alpha=0.5)

                ax.set_xlabel('Position in Motif')
                ax.set_ylabel('Property Value')
                ax.set_title('Amino Acid Property Profile')
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

            with tabs[1]:
                fig = plot_weighted_properties(hit_data, selected_sequence, selected_position)
                st.pyplot(fig)

            with tabs[2]:
                st.markdown("#### Confidence Profile")
                fig, ax = plt.subplots(figsize=(10, 4))
                center = (int(selected_position.split('-')[0]) + int(selected_position.split('-')[1])) // 2
                x_range = list(range(max(1, center - 50), min(len(full_sequence), center + 51)))
                y_values = []
                g_score = hit_data["weighted_properties"]["G"]

                for x in x_range:
                    dist = abs(x - center)
                    if dist == 0:
                        y_values.append(g_score * 10)
                    else:
                        y_values.append(g_score * 10 * math.exp(-0.01 * (dist ** 2)))

                ax.plot(x_range, y_values, 'b-')
                ax.fill_between(x_range, y_values, alpha=0.3)
                ax.axhline(y=3, color='r', linestyle='--', alpha=0.5, label='Threshold')
                ax.set_xlabel('Sequence Position')
                ax.set_ylabel('Confidence Score')
                ax.set_title('Confidence Profile Around Match')
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

            st.subheader("Interpretation Guide")
            st.markdown("""
            - **Green (>0.7)**: High confidence, closest to experimentally validated centers
            - **Orange (0.3-0.7)**: Medium confidence
            - **Red (<0.3)**: Low confidence

            Recommended to focus on matches with:
            - Two or more green physicochemical values (GH, GW, GP)
            - Green overall G value
            - No red values
            """)

            if analysis_type == "AC-Pred":
                st.markdown("""
                **AC-Pred Specific:**

                In AC motif pattern `[KSR]X[DE]X(10)[KR]X(0,2)[DE]`
                """)
            else:
                st.markdown("""
                **GC-Pred Specific:**

                In GC motif pattern `[RK]X[SCG]X(10)[KR]X(0,2)[DE]`
               
                """)

if __name__ == "__main__":
    main()