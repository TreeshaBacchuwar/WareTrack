import sys
import os
import pandas as pd
import plotly.express as px
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io
import math

# Dynamically determine the project root
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of app.py (frontend/)
project_root = os.path.abspath(os.path.join(script_dir, ".."))  # Go up one level to project root
sys.path.append(project_root)  # Add project root to Python path

# Import from backend
from backend.inventory import Inventory, Item

# Initialize inventory
inventory = Inventory()
try:
    inventory.load_from_file()
except Exception as e:
    st.error(f"Failed to load inventory: {str(e)}")

# Streamlit App Configuration
st.set_page_config(page_title="WareTrack", layout="wide")
st.title("📦 WareTrack")

# Explicitly initialize session state for low_stock_threshold
if "low_stock_threshold" not in st.session_state:
    st.session_state.low_stock_threshold = 10

# Function to generate PDF report
def generate_pdf_report(inventory):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Styles for the report
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    # Title
    elements.append(Paragraph("Inventory Report", title_style))
    elements.append(Spacer(1, 12))

    # Summary Section
    total_items = len(inventory.items_by_id)
    total_value = inventory.total_inventory_value()
    low_stock_count = len(inventory.get_low_stock_items(threshold=st.session_state.low_stock_threshold))

    summary_text = f"""
    <b>Summary</b><br/>
    Total Items: {total_items}<br/>
    Total Value: Rs {total_value:.2f}<br/>
    Low Stock Items (Threshold: {st.session_state.low_stock_threshold}): {low_stock_count}
    """
    elements.append(Paragraph(summary_text, normal_style))
    elements.append(Spacer(1, 24))

    # Inventory Table
    elements.append(Paragraph("Current Inventory", styles["Heading2"]))
    elements.append(Spacer(1, 12))

    # Prepare data for the table
    items = list(inventory.items_by_id.values())
    if items:
        data = [["ID", "Name", "Quantity", "Price", "Category"]]  # Table headers
        for item in items:
            data.append([item.id, item.name, item.quantity, item.price, item.category])
        
        # Create the table
        table = Table(data)
        table.setStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ])
        elements.append(table)
    else:
        elements.append(Paragraph("No items in inventory.", normal_style))

    # Build the PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

# Sidebar for unified navigation
st.sidebar.title("Navigation")
selected_option = st.sidebar.radio("Go to", [
    "Inventory", "Dashboard", "Value Trend", "Transaction History",
    "Add Item", "Update Item", "Remove Item", "Low Stock"
])

st.sidebar.markdown("---")
st.sidebar.markdown("#### 📊 Inventory Overview")
st.sidebar.metric("Total Items", len(inventory.items_by_id))
st.sidebar.metric("Total Value", f"Rs {inventory.total_inventory_value()}")
st.sidebar.metric("Low Stock Items", len(inventory.get_low_stock_items(threshold=10)))

st.markdown(
    """
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: bold;
        color: #0078FF;
    }
    div[data-testid="stDataFrame"] table {
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom styles
st.markdown(
    """
    <style>
        /* Centered Heading with Spacing */
        .title {
            text-align: center; 
            font-size: 36px; 
            font-weight: bold; 
            color: #ffffff;
            margin-bottom: 20px;
        }

        /* Input Fields */
        .search-box, .filter-box, .sort-box {
            background-color: #2a2a2a;
            color: white;
            padding: 12px;
            border-radius: 10px;
            border: 1px solid #444;
            width: 100%;
            transition: 0.3s ease-in-out;
        }
        .search-box:hover, .filter-box:hover, .sort-box:hover {
            border: 1px solid #ffcc00;
            background-color: #333;
        }

        /* Inventory Table */
        .dataframe {
            background-color: #1e1e1e;
            color: white;
            border-radius: 12px;
        }

        /* Table Styling */
        table tbody tr:nth-child(even) {
            background-color: #2b2b2b !important;
        }
        table tbody tr:hover {
            background-color: #444 !important;
            transition: 0.3s ease-in-out;
        }

        /* Stylish Buttons */
        .stButton>button {
            background-color: #ffcc00;
            color: black;
            border-radius: 10px;
            padding: 10px 16px;
            font-weight: bold;
            transition: 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #ffaa00;
        }

        /* Dashboard Title */
        .dashboard-title {
            text-align: center;
            font-size: 38px;
            font-weight: bold;
            color: #ffcc00;
            margin-bottom: 30px;
            margin-top: 20px;
        }
        
        /* Metric Cards */
        .metric-card {
            background: #222;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 2px 2px 15px rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .metric-card:hover {
            transform: scale(1.05);
            box-shadow: 2px 2px 15px rgba(255, 255, 255, 0.4);
        }
        
        .metric-title {
            font-size: 22px;
            font-weight: bold;
            color: #00bfff;
        }
        .metric-value {
            font-size: 30px;
            font-weight: bold;
            color: white;
        }

        /* Transaction History Styling */
        .transaction-box {
            padding: 12px;
            margin-bottom: 10px;
            background-color: #1e1e1e;
            border-left: 5px solid #ffcc00;
            border-radius: 8px;
            color: #ffffff;
            font-size: 18px;
        }
        .timestamp {
            color: #bbbbbb;
            font-size: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Conditional display based on selected option
if selected_option == "Inventory":
    st.markdown("<h1 class='title'>📋 Current Inventory</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        search_keyword = st.text_input("🔍 Search by ID or Name", key="search", help="Type to search an item")
    
    with col2:
        categories = set(item.category for item in inventory.items_by_id.values())
        selected_category = st.selectbox("📂 Filter by Category", ["All"] + sorted(categories))
    
    with col3:
        sort_by = st.selectbox("🔽 Sort by", ["ID", "Name", "Quantity", "Price"])
    
    # Apply filtering and sorting
    filtered_items = list(inventory.items_by_id.values())
    if search_keyword:
        search_keyword = search_keyword.lower()
        filtered_items = [item for item in filtered_items if search_keyword in str(item.id) or search_keyword in item.name.lower()]
    if selected_category != "All":
        filtered_items = [item for item in filtered_items if item.category == selected_category]
    
    sort_key = {"ID": "id", "Name": "name", "Quantity": "quantity", "Price": "price"}
    filtered_items.sort(key=lambda x: getattr(x, sort_key[sort_by]))
    
    if filtered_items:
        df = pd.DataFrame([{"ID": item.id, "Name": item.name, "Quantity": item.quantity, "Price": item.price, "Category": item.category} for item in filtered_items])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No items match the search/filter criteria.")

elif selected_option == "Dashboard":
    st.markdown("<h1 class='dashboard-title'>📊 Inventory Dashboard</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>Total Items</div><div class='metric-value'>{len(inventory.items_by_id)}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>Total Value</div><div class='metric-value'>Rs {inventory.total_inventory_value()}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>Low Stock Items</div><div class='metric-value'>{len(inventory.get_low_stock_items(threshold=st.session_state.low_stock_threshold))}</div></div>", unsafe_allow_html=True)
    
    df_value = pd.DataFrame(
        [{"Category": item.category, "Value": item.quantity * item.price} for item in inventory.items_by_id.values()]
    )
    
    fig_value = px.bar(df_value.groupby("Category").sum().reset_index(), x="Category", y="Value", title="Inventory Value by Category", color="Category")
    fig_value.update_traces(width=0.1)
    st.plotly_chart(fig_value, use_container_width=True)

    fig_pie = px.pie(df_value, names="Category", values="Value", title="📊 Inventory Distribution by Category", hole=0.3)
    fig_pie.update_traces(textinfo="percent+label", hoverinfo="label+value")
    fig_pie.update_layout(plot_bgcolor="#1e1e1e", paper_bgcolor="#1e1e1e", font=dict(color="white"), title_x=0.3)
    st.plotly_chart(fig_pie, use_container_width=True)

    # Add download button for PDF report
    if st.button("Download Report as PDF"):
        pdf_buffer = generate_pdf_report(inventory)
        st.download_button(
            label="Download PDF",
            data=pdf_buffer,
            file_name="inventory_report.pdf",
            mime="application/pdf"
        )

elif selected_option == "Value Trend":
    st.header("📈 Inventory Value Trend")
    if inventory.inventory_value_history:
        df = pd.DataFrame(
            [
                {"Timestamp": timestamp, "Category": category, "Value": value}
                for timestamp, _, category_values in inventory.inventory_value_history
                for category, value in category_values.items()
            ]
        )
        if not df.empty:
            fig = px.area(df, x="Timestamp", y="Value", color="Category", title="Inventory Value Over Time by Category")
            fig.update_layout(xaxis_title="Time", yaxis_title="Inventory Value", xaxis_tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No category data available for inventory value trend.")
    else:
        st.info("No data available for inventory value trend.")

elif selected_option == "Transaction History":
    st.markdown(
        "<h1 style='text-align: center; color: #f8f9fa;'>📜 Transaction History</h1>", 
        unsafe_allow_html=True
    )
    if inventory.transaction_history:
        st.markdown(
            """
            <style>
                .transaction-box {
                    padding: 12px;
                    margin-bottom: 10px;
                    background-color: #1e1e1e;
                    border-left: 5px solid #ffcc00;
                    border-radius: 8px;
                    color: #ffffff;
                    font-size: 18px;
                }
                .timestamp {
                    color: #bbbbbb;
                    font-size: 14px;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        for timestamp, action in reversed(inventory.transaction_history):
            st.markdown(
                f"""
                <div class="transaction-box">
                    <span class="timestamp">{timestamp}</span><br>
                    {action}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No transactions recorded.")

elif selected_option == "Add Item":
    st.header("➕ Add New Item")
    with st.form("add_item_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            item_id = st.number_input("Item ID", min_value=1, step=1)
            item_quantity = st.number_input("Quantity", min_value=0, step=1)
        with col2:
            item_name = st.text_input("Item Name")
            item_price = st.number_input("Price", min_value=0.01, step=0.01)
        with col3:
            item_category = st.text_input("Category")
        submit = st.form_submit_button("Add Item")
    
    if submit:
        if not item_name or not item_category:
            st.error("Name and Category are required!")
        else:
            try:
                new_item = Item(item_id, item_name, item_quantity, item_price, item_category)
                inventory.add_item(new_item)
                inventory.save_to_file()
                st.success("Item added successfully!")
            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Error adding item: {str(e)}")

elif selected_option == "Update Item":
    st.header("🔄 Update Item")
    with st.form("update_item_form"):
        item_id = st.number_input("Item ID", min_value=1, step=1)
        new_quantity = st.number_input("New Quantity", min_value=0, step=1)
        new_price = st.number_input("New Price", min_value=0.01, step=0.01)
        submit = st.form_submit_button("Update Item")
    
    if submit:
        try:
            inventory.update_item(item_id, new_quantity=new_quantity, new_price=new_price)
            inventory.save_to_file()
            st.success("Item updated successfully!")
        except ValueError as e:
            st.error(str(e))

elif selected_option == "Remove Item":
    st.header("❌ Remove Item")
    with st.form("remove_item_form"):
        item_id = st.number_input("Item ID", min_value=1, step=1)
        submit = st.form_submit_button("Remove Item")
    
    if submit:
        try:
            inventory.remove_item(item_id)
            inventory.save_to_file()
            st.success("Item removed successfully!")
        except ValueError as e:
            st.error(str(e))

elif selected_option == "Low Stock":
    st.header("⚠️ Low Stock Alerts")
    # Set low stock threshold
    st.session_state.low_stock_threshold = st.number_input(
        "Set Low Stock Threshold", 
        min_value=1, 
        value=st.session_state.low_stock_threshold, 
        step=1
    )
    
    # Get low-stock items
    low_stock_items = inventory.get_low_stock_items(threshold=st.session_state.low_stock_threshold)
    if low_stock_items:
        st.table(pd.DataFrame([{"ID": item.id, "Name": item.name, "Quantity": item.quantity, "Category": item.category} for item in low_stock_items]))
    else:
        st.info("No low-stock items.")