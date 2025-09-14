import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import io

# Configure Streamlit page with dark theme
st.set_page_config(
    page_title="Map Generator - Blue Dark Theme",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for blue dark theme
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0f1629 25%, #1a237e 75%, #1565c0 100%);
        color: #e1effe;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        backdrop-filter: blur(15px);
    }
    
    /* Title styling */
    .main .block-container {
        padding-top: 2rem;
    }
    
    h1 {
        color: #93c5fd;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
    }
    
    h2, h3 {
        color: #93c5fd;
        margin-bottom: 1rem;
    }
    
    /* Input widgets styling */
    .stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.9);
        border: 2px solid rgba(37, 99, 235, 0.3);
        border-radius: 8px;
        color: #e1effe;
    }
    
    .stTextInput > div > div > input {
        background: rgba(15, 23, 42, 0.9);
        border: 2px solid rgba(37, 99, 235, 0.3);
        border-radius: 8px;
        color: #e1effe;
    }
    
    .stSlider > div > div > div {
        background: rgba(15, 23, 42, 0.9);
        border-radius: 8px;
    }
    
    .stMultiSelect > div > div {
        background: rgba(15, 23, 42, 0.9);
        border: 2px solid rgba(37, 99, 235, 0.3);
        border-radius: 8px;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        backdrop-filter: blur(15px);
        border: 2px dashed #2563eb;
        border-radius: 15px;
        padding: 2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(29, 78, 216, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(29, 78, 216, 0.4);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(5, 150, 105, 0.3);
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #047857 0%, #065f46 100%);
        transform: translateY(-2px);
    }
    
    /* Cards and containers */
    .element-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        border: 1px solid rgba(37, 99, 235, 0.2);
        margin: 1rem 0;
        padding: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    
    /* Metric styling */
    .metric-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        border: 1px solid rgba(37, 99, 235, 0.2);
        padding: 1rem;
        text-align: center;
    }
    
    /* Alert styling */
    .stAlert {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.2) 0%, rgba(185, 28, 28, 0.2) 100%);
        border-left: 4px solid #dc2626;
        color: #fca5a5;
        backdrop-filter: blur(15px);
    }
    
    /* Success styling */
    .stSuccess {
        background: linear-gradient(135deg, rgba(5, 150, 105, 0.2) 0%, rgba(4, 120, 87, 0.2) 100%);
        border-left: 4px solid #059669;
        color: #6ee7b7;
        backdrop-filter: blur(15px);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("MAP GENERATOR")
st.markdown("<h3 style='text-align: center; color: #9ca3af; margin-bottom: 2rem;'>Create customized maps with your data</h3>", unsafe_allow_html=True)

# Load the shapefile
@st.cache_data
def load_shapefile():
    return gpd.read_file("https://raw.githubusercontent.com/mohamedsillahkanu/si/2b7f982174b609f9647933147dec2a59a33e736a/Chiefdom%202021.shp")

try:
    gdf = load_shapefile()
except Exception as e:
    st.error(f"Error loading shapefile: {e}")
    st.stop()

# Define color options with blue theme additions
nice_colors = {
    "Deep Blue": "#1e3a8a",
    "Royal Blue": "#2563eb",
    "Sky Blue": "#3b82f6",
    "Light Blue": "#60a5fa",
    "Cyan": "#06b6d4",
    "Teal": "#0d9488",
    "Emerald": "#059669",
    "Green": "#16a34a",
    "Lime": "#65a30d",
    "Yellow": "#eab308",
    "Amber": "#f59e0b",
    "Orange": "#ea580c",
    "Red": "#dc2626",
    "Rose": "#e11d48",
    "Pink": "#ec4899",
    "Purple": "#9333ea",
    "Violet": "#7c3aed",
    "Indigo": "#4f46e5",
    "Black": "#000000",
    "Gray": "#6b7280",
    "Silver": "#9ca3af",
    "White": "#ffffff"
}

# Display colors in a grid with blue theme styling
st.subheader("Available Colors")
color_cols = st.columns(6)
for i, (color_name, hex_code) in enumerate(nice_colors.items()):
    with color_cols[i % 6]:
        text_color = "#000000" if color_name in ["White", "Silver", "Yellow", "Lime"] else "#ffffff"
        st.markdown(
            f"""<div style="
                background-color:{hex_code}; 
                padding:8px; 
                margin:4px; 
                color:{text_color}; 
                border:2px solid rgba(37, 99, 235, 0.3);
                border-radius:8px;
                text-align:center;
                font-size:12px;
                font-weight:600;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                backdrop-filter: blur(10px);
            ">{color_name}</div>""",
            unsafe_allow_html=True
        )

# File upload with enhanced styling
st.subheader("Data Upload")
uploaded_file = st.file_uploader(
    "Upload Excel or CSV file", 
    type=["xlsx", "csv"],
    help="Upload your data file to create a customized map"
)

if uploaded_file is not None:
    try:
        # Read the uploaded file
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        
        st.success(f"Successfully loaded {len(df)} rows of data!")
        
        # Configuration section
        st.subheader("Map Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            available_columns = [col for col in df.columns if col not in ['FIRST_DNAM', 'FIRST_CHIE', 'adm3']]
            map_column = st.selectbox("Select Map Column:", available_columns)
            map_title = st.text_input("Map Title:", placeholder="Enter your map title")
            legend_title = st.text_input("Legend Title:", placeholder="Enter legend title")
        
        with col2:
            image_name = st.text_input("Image Name:", value="Generated_Map")
            font_size = st.slider("Font Size (for Map Title):", 8, 24, 16)
        
        # Line settings
        st.subheader("Line Settings")
        line_col1, line_col2 = st.columns(2)
        
        with line_col1:
            line_color = st.selectbox("Select Default Line Color:", list(nice_colors.keys()), index=0)
            line_width = st.slider("Select Default Line Width:", 0.1, 3.0, 0.5, 0.1)
        
        with line_col2:
            missing_value_color = st.selectbox("Select Color for Missing Values:", list(nice_colors.keys()), index=3)
            missing_value_label = st.text_input("Label for Missing Values:", value="No Data")
        
        # Category selection
        st.subheader("Category Selection")
        unique_values = sorted(df[map_column].dropna().unique().tolist())
        selected_categories = st.multiselect(
            f"Select Categories for {map_column}:", 
            unique_values, 
            default=unique_values,
            help="Choose which categories to display on the map"
        )
        
        if selected_categories:
            df[map_column] = pd.Categorical(df[map_column], categories=selected_categories, ordered=True)
            category_counts = df[map_column].value_counts().to_dict()
            
            # Color assignment section
            st.subheader("Color Assignment")
            color_mapping = {}
            
            # Create columns for color selection
            color_select_cols = st.columns(min(3, len(selected_categories)))
            
            for i, category in enumerate(selected_categories):
                with color_select_cols[i % len(color_select_cols)]:
                    default_color = list(nice_colors.keys())[i % len(nice_colors)]
                    selected_color = st.selectbox(
                        f"Color for '{category}':", 
                        list(nice_colors.keys()), 
                        index=list(nice_colors.keys()).index(default_color),
                        key=f"color_{category}"
                    )
                    color_mapping[category] = nice_colors[selected_color]
                    
                    # Show preview of selected color
                    st.markdown(
                        f"""<div style="
                            background-color:{nice_colors[selected_color]}; 
                            padding:4px; 
                            margin:2px 0; 
                            color:{'#000000' if selected_color in ['White', 'Silver', 'Yellow'] else '#ffffff'}; 
                            border-radius:4px;
                            text-align:center;
                            font-size:10px;
                        ">Preview</div>""",
                        unsafe_allow_html=True
                    )
            
            # Advanced settings in expandable section
            with st.expander("Advanced Settings", expanded=False):
                st.subheader("Boundary Line Settings")
                adv_col1, adv_col2 = st.columns(2)
                
                with adv_col1:
                    first_dnam_color = st.selectbox("Color for FIRST_DNAM:", list(nice_colors.keys()), index=0)
                    first_dnam_width = st.slider("Line Width for FIRST_DNAM:", 0.1, 3.0, 1.0, 0.1)
                
                with adv_col2:
                    first_chie_color = st.selectbox("Color for FIRST_CHIE:", list(nice_colors.keys()), index=20)
                    first_chie_width = st.slider("Line Width for FIRST_CHIE:", 0.1, 3.0, 0.5, 0.1)
            else:
                # Default values when expander is closed
                first_dnam_color = "Black"
                first_dnam_width = 1.0
                first_chie_color = "Silver"
                first_chie_width = 0.5
            
            # Generate map button
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Generate Map", type="primary", use_container_width=True):
                with st.spinner("Generating your customized map..."):
                    try:
                        # Set matplotlib style for dark theme
                        plt.style.use('dark_background')
                        
                        # Create figure with dark theme
                        fig, ax = plt.subplots(figsize=(12, 10), facecolor='#0a0e1a')
                        ax.set_facecolor('#ffffff')  # White background for the map area
                        
                        # Plot the boundary of the entire map
                        gdf.boundary.plot(ax=ax, linewidth=line_width, edgecolor=nice_colors[line_color])
                        
                        # Create legend handles manually
                        legend_handles = []
                        
                        # Plot each category
                        for category in selected_categories:
                            if category in df[map_column].unique():
                                # Find chiefdoms that match this category
                                chiefdoms_in_category = df[df[map_column] == category]["FIRST_CHIE"].unique()
                                # Get the GDF subset for these chiefdoms
                                sub_gdf = gdf[gdf["FIRST_CHIE"].isin(chiefdoms_in_category)]
                                
                                if not sub_gdf.empty:
                                    # Plot this category on the map
                                    sub_gdf.plot(
                                        ax=ax, 
                                        color=color_mapping[category], 
                                        edgecolor=nice_colors[line_color],
                                        linewidth=line_width
                                    )
                                    
                                    # Create a patch for the legend
                                    count = category_counts.get(category, 0)
                                    legend_handles.append(Patch(
                                        color=color_mapping[category], 
                                        label=f"{category} ({count})"
                                    ))
                        
                        # Handle missing values
                        missing_gdf = gdf[~gdf["FIRST_CHIE"].isin(df[df[map_column].notna()]["FIRST_CHIE"])]
                        if not missing_gdf.empty:
                            missing_gdf.plot(
                                ax=ax, 
                                color=nice_colors[missing_value_color], 
                                edgecolor=nice_colors[line_color],
                                linewidth=line_width
                            )
                            missing_count = len(missing_gdf)
                            legend_handles.append(Patch(
                                color=nice_colors[missing_value_color], 
                                label=f"{missing_value_label} ({missing_count})"
                            ))
                        
                        # Plot boundary lines
                        gdf.plot(ax=ax, color="none", edgecolor=nice_colors[first_dnam_color], linewidth=first_dnam_width)
                        gdf.plot(ax=ax, color="none", edgecolor=nice_colors[first_chie_color], linewidth=first_chie_width)
                        
                        # Add custom legend with enhanced styling
                        legend = ax.legend(
                            handles=legend_handles,
                            title=legend_title, 
                            loc='center left',
                            fontsize=12,
                            title_fontsize=14,
                            bbox_to_anchor=(1, 0.5),
                            frameon=True,
                            facecolor='#f8f9fa',
                            edgecolor='#1e3a8a',
                            framealpha=0.95
                        )
                        
                        # Style legend title
                        legend.get_title().set_fontweight('bold')
                        legend.get_title().set_color('#1e3a8a')
                        
                        # Add title with enhanced styling
                        ax.set_title(
                            map_title, 
                            fontsize=font_size + 2, 
                            fontweight='bold',
                            color='#1e3a8a',
                            pad=20
                        )
                        
                        # Remove axis
                        ax.set_xticks([])
                        ax.set_yticks([])
                        ax.set_frame_on(False)
                        
                        # Display map in Streamlit
                        st.pyplot(fig, use_container_width=True)
                        
                        # Save map as a PNG file
                        img_buffer = io.BytesIO()
                        fig.savefig(
                            img_buffer, 
                            format="png", 
                            dpi=300, 
                            bbox_inches="tight",
                            facecolor='white',
                            edgecolor='none'
                        )
                        img_buffer.seek(0)
                        
                        # Add download button with success message
                        st.success("Map generated successfully!")
                        st.download_button(
                            label="Download Map as PNG",
                            data=img_buffer,
                            file_name=f"{image_name}.png",
                            mime="image/png",
                            type="primary"
                        )
                        
                        # Clear the plot to free memory
                        plt.close(fig)
                        
                    except Exception as e:
                        st.error(f"An error occurred while generating the map: {e}")
                        st.error("Please check your data and try again.")
    
    except Exception as e:
        st.error(f"Error reading the uploaded file: {e}")
        st.error("Please ensure your file is properly formatted.")

else:
    # Instructions when no file is uploaded
    st.info("Please upload an Excel or CSV file to get started.")
    
    with st.expander("File Format Requirements", expanded=False):
        st.markdown("""
        **Your data file should contain:**
        - A column named `FIRST_CHIE` that matches the chiefdom names in the shapefile
        - At least one data column for mapping
        - Properly formatted headers
        
        **Supported file formats:**
        - Excel files (.xlsx)
        - CSV files (.csv)
        """)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """<div style='text-align: center; color: #6b7280; padding: 2rem; border-top: 1px solid rgba(37, 99, 235, 0.2);'>
    Map Generator Tool | Built with Streamlit & GeoPandas
    </div>""", 
    unsafe_allow_html=True
)
