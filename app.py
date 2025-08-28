import streamlit as st
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="🔋 Battery Cell Manager",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
    }
    
    .cell-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cells_data' not in st.session_state:
    st.session_state.cells_data = {}
if 'cell_types' not in st.session_state:
    st.session_state.cell_types = []

# Main header
st.markdown('<h1 class="main-header">🔋 Battery Cell Management System</h1>', unsafe_allow_html=True)

# Sidebar for cell configuration
with st.sidebar:
    st.markdown("## 🔧 Cell Configuration")
    
    # Number of cells selector
    num_cells = st.slider("Number of Cells", min_value=1, max_value=12, value=8, key="num_cells")
    
    st.markdown("### Select Cell Types")
    
    # Dynamic cell type selection
    cell_types = []
    for i in range(num_cells):
        cell_type = st.selectbox(
            f"Cell #{i+1} Type",
            options=["LFP", "NMC"],
            key=f"cell_type_{i}",
            help="LFP: Lithium Iron Phosphate, NMC: Nickel Manganese Cobalt"
        )
        cell_types.append(cell_type.lower())
    
    # Button to generate cells
    if st.button("🚀 Generate Cells", type="primary", use_container_width=True):
        st.session_state.cell_types = cell_types
        cells_data = {}
        
        for idx, cell_type in enumerate(cell_types, start=1):
            cell_key = f"cell_{idx}_{cell_type}"
            voltage = 3.2 if cell_type == "lfp" else 3.6
            min_voltage = 2.8 if cell_type == "lfp" else 3.2
            max_voltage = 3.6 if cell_type == "lfp" else 4.0
            current = 0.0
            temp = round(random.uniform(25, 40), 1)
            capacity = round(voltage * current, 2)
            
            cells_data[cell_key] = {
                "voltage": voltage,
                "current": current,
                "temp": temp,
                "capacity": capacity,
                "min_voltage": min_voltage,
                "max_voltage": max_voltage,
                "type": cell_type.upper()
            }
        
        st.session_state.cells_data = cells_data
        st.success(f"✅ Generated {num_cells} cells successfully!")

# Main content area
if st.session_state.cells_data:
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Cell Overview", "⚡ Current Input", "📈 Analytics", "📋 Data Table"])
    
    with tab1:
        st.markdown("## 📊 Cell Overview")
        
        # Display cells in a grid layout
        cols = st.columns(3)
        for idx, (cell_key, cell_data) in enumerate(st.session_state.cells_data.items()):
            with cols[idx % 3]:
                # Determine color based on cell type
                color = "🟢" if cell_data["type"] == "LFP" else "🔵"
                
                st.markdown(f"""
                <div class="cell-card">
                    <h3>{color} {cell_key.replace('_', ' ').title()}</h3>
                    <div class="metric-card">
                        <strong>🔋 Voltage:</strong> {cell_data['voltage']} V<br>
                        <strong>⚡ Current:</strong> {cell_data['current']} A<br>
                        <strong>🌡 Temperature:</strong> {cell_data['temp']} °C<br>
                        <strong>⚡ Capacity:</strong> {cell_data['capacity']} Wh<br>
                        <strong>📊 Range:</strong> {cell_data['min_voltage']}-{cell_data['max_voltage']} V
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("## ⚡ Current Input Configuration")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Adjust Current Values")
            
            # Create current input fields
            updated_data = st.session_state.cells_data.copy()
            
            for cell_key in st.session_state.cells_data.keys():
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    current = st.number_input(
                        f"Current for {cell_key.replace('_', ' ').title()}",
                        min_value=0.0,
                        max_value=10.0,
                        value=float(st.session_state.cells_data[cell_key]["current"]),
                        step=0.1,
                        key=f"current_{cell_key}",
                        help="Enter current in Amperes"
                    )
                with col_b:
                    st.markdown(f"*Type:* {st.session_state.cells_data[cell_key]['type']}")
                
                # Update the data
                voltage = updated_data[cell_key]["voltage"]
                updated_data[cell_key]["current"] = current
                updated_data[cell_key]["capacity"] = round(voltage * current, 2)
            
            if st.button("🔄 Update All Currents", type="primary"):
                st.session_state.cells_data = updated_data
                st.success("✅ All currents updated successfully!")
                st.rerun()
        
        with col2:
            st.markdown("### 📊 Quick Stats")
            total_capacity = sum(cell["capacity"] for cell in st.session_state.cells_data.values())
            avg_temp = sum(cell["temp"] for cell in st.session_state.cells_data.values()) / len(st.session_state.cells_data)
            total_current = sum(cell["current"] for cell in st.session_state.cells_data.values())
            
            st.metric("Total Capacity", f"{total_capacity:.2f} Wh")
            st.metric("Average Temperature", f"{avg_temp:.1f} °C")
            st.metric("Total Current", f"{total_current:.1f} A")
            
            # Cell type distribution
            lfp_count = sum(1 for cell in st.session_state.cells_data.values() if cell["type"] == "LFP")
            nmc_count = len(st.session_state.cells_data) - lfp_count
            
            st.markdown("### Cell Distribution")
            st.markdown(f"🟢 LFP Cells: {lfp_count}")
            st.markdown(f"🔵 NMC Cells: {nmc_count}")
    
    with tab3:
        st.markdown("## 📈 Analytics Dashboard")
    
    # Prepare data for visualization
    df = pd.DataFrame(st.session_state.cells_data).T
    df['cell_name'] = df.index

    # 🔑 Ensure numeric columns are proper floats
    df['capacity'] = pd.to_numeric(df['capacity'], errors='coerce')
    df['current'] = pd.to_numeric(df['current'], errors='coerce')
    df['voltage'] = pd.to_numeric(df['voltage'], errors='coerce')
    df['temp'] = pd.to_numeric(df['temp'], errors='coerce')

    col1, col2 = st.columns(2)
    
    with col1:
        # Voltage vs Current scatter plot
        fig1 = px.scatter(
            df, 
            x='voltage', 
            y='current',
            color='type',
            size='capacity',   # ✅ now guaranteed numeric
            hover_data=['temp', 'capacity'],
            title="🔋 Voltage vs Current Analysis",
            color_discrete_map={'LFP': '#2E8B57', 'NMC': '#4169E1'}
        )
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Temperature distribution
        fig3 = px.histogram(
            df,
            x='temp',
            color='type',
            title="🌡 Temperature Distribution",
            nbins=10,
            color_discrete_map={'LFP': '#2E8B57', 'NMC': '#4169E1'}
        )
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Capacity comparison bar chart
        fig2 = px.bar(
            df,
            x='cell_name',
            y='capacity',
            color='type',
            title="⚡ Cell Capacity Comparison",
            color_discrete_map={'LFP': '#2E8B57', 'NMC': '#4169E1'}
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Cell type pie chart
        type_counts = df['type'].value_counts()
        fig4 = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title="📊 Cell Type Distribution",
            color_discrete_map={'LFP': '#2E8B57', 'NMC': '#4169E1'}
        )
        fig4.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig4, use_container_width=True)

    
    with tab4:
        st.markdown("## 📋 Detailed Data Table")
        
        # Display data as a formatted table
        display_df = pd.DataFrame(st.session_state.cells_data).T
        display_df.index.name = "Cell ID"
        
        # Format the dataframe for better display
        display_df_formatted = display_df.round(2)
        display_df_formatted.columns = [col.replace('_', ' ').title() for col in display_df_formatted.columns]
        
        st.dataframe(
            display_df_formatted,
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = display_df_formatted.to_csv()
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name="battery_cell_data.csv",
            mime="text/csv",
            use_container_width=True
        )
else:
    # Welcome message when no cells are configured
    st.markdown("""
    <div style="text-align: center; padding: 4rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; color: white; margin: 2rem 0;">
        <h2>🚀 Welcome to Battery Cell Manager!</h2>
        <p style="font-size: 1.2rem; margin: 2rem 0;">Configure your battery cells using the sidebar to get started.</p>
        <p>✨ Features:</p>
        <p>🔋 Support for LFP and NMC cell types<br>
        ⚡ Real-time current and capacity calculations<br>
        📊 Interactive analytics and visualizations<br>
        📱 Responsive and beautiful UI</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; padding: 1rem;'>"
    "🔋 Battery Cell Management System | Built with ❤ using Streamlit"
    "</div>", 
    unsafe_allow_html=True
)