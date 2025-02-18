import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up page with futuristic dark theme
st.set_page_config(page_title="Data Transformer", layout="wide")

# Custom CSS - Futuristic Dark Theme
st.markdown(
    """
    <style>
        /* Background - Cyberpunk Style */
        .stApp {
            background: linear-gradient(135deg, #0f0f0f, #1c1c1c);
            color: #dcdcdc;
            font-family: 'Arial', sans-serif;
        }

        /* Sidebar - Neon Glow Effect */
        [data-testid="stSidebar"] {
            background: rgba(20, 20, 20, 0.9);
            border-right: 2px solid #00ffcc;
            box-shadow: 5px 0px 15px rgba(0, 255, 204, 0.4);
        }

        /* File Upload Box - Glowing Neon */
        div[data-testid="stFileUploader"] {
            border: 2px dashed #00ffcc;
            border-radius: 12px;
            padding: 15px;
            transition: all 0.3s ease-in-out;
        }
        div[data-testid="stFileUploader"]:hover {
            border-color: #ff00ff;
            transform: scale(1.02);
        }

        /* Buttons - Neon Effects */
        .stButton > button {
            background: linear-gradient(90deg, #00ffcc, #ff00ff);
            color: white;
            border-radius: 12px;
            padding: 12px 20px;
            font-weight: bold;
            transition: all 0.3s ease-in-out;
            border: none;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #ff00ff, #00ffcc);
            transform: scale(1.05);
            box-shadow: 0px 0px 15px rgba(255, 0, 255, 0.7);
        }

        /* Download Buttons */
        .stDownloadButton > button {
            background: linear-gradient(90deg, #ffcc00, #ff6600);
            color: white;
            border-radius: 12px;
            padding: 12px 20px;
            transition: all 0.3s ease-in-out;
            font-weight: bold;
        }
        .stDownloadButton > button:hover {
            background: linear-gradient(90deg, #ff6600, #ffcc00);
            transform: scale(1.05);
            box-shadow: 0px 0px 15px rgba(255, 165, 0, 0.7);
        }

        /* Tables */
        .stDataFrame {
            border-radius: 12px;
            overflow: hidden;
            border: 2px solid #00ffcc;
            box-shadow: 0px 0px 20px rgba(0, 255, 204, 0.3);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar - Futuristic Glow Theme
st.sidebar.title("🧨Data Transformer🧨")
st.sidebar.write("✨Convert, clean, and visualize your **Excel & CSV** files!")

# Main Title
st.title("📂 Transform Your Files with Cyberpunk AI 💾")
st.write("🔄 Convert files, clean data, and visualize in **style**!")

# File Upload Section - Futuristic Glow Box
uploaded_files = st.file_uploader(
    "📤 Drag & Drop or Upload your Excel/CSV file",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

# Progress Bar Effect
if uploaded_files:
    st.success("📂 File(s) Uploaded Successfully!")
    progress_bar = st.progress(0)
    
    for i in range(100):
        progress_bar.progress(i + 1)
    
    st.success("✅ Processing Complete!")

    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read the file based on type
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"❌ Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"⚠️ Error reading file: {e}")
            continue

        # Display File Information
        st.markdown(f"### 📄 `{file.name}`")
        st.write(f"**File Size:** {round(file.size / 1024, 2)} KB")
        st.write("🔍 **Data Preview:**")
        st.dataframe(df.head())

        # Dataset Summary
        st.write("📊 **Dataset Summary:**")
        st.write(df.describe())

        # Data Cleaning Section
        st.subheader("🧹 Data Cleaning")
        clean_col1, clean_col2 = st.columns(2)

        with clean_col1:
            if st.button(f"🗑 Remove Duplicates from `{file.name}`"):
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates removed!")

        with clean_col2:
            if st.button(f"📉 Fill Missing Values for `{file.name}`"):
                numeric_cols = df.select_dtypes(include=["number"]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("✅ Missing values filled!")

        # Select Columns to Keep
        st.subheader("🎯 Choose Columns to Keep")
        selected_columns = st.multiselect(f"Choose columns for `{file.name}`", df.columns, default=df.columns)
        df = df[selected_columns]

        # Rename Columns
        st.subheader("✏️ Rename Columns")
        new_column_names = {}
        for col in selected_columns:
            new_name = st.text_input(f"Rename `{col}`", col)
            new_column_names[col] = new_name
        df.rename(columns=new_column_names, inplace=True)

        # Data Visualization with Enhanced Charts
        st.subheader("📈 Data Visualization")
        if st.checkbox(f"📊 Show Visualization for `{file.name}`"):
            numeric_df = df.select_dtypes(include=["number"])
            if not numeric_df.empty and numeric_df.shape[1] >= 2:
                st.bar_chart(numeric_df.iloc[:, :2])
            else:
                st.warning("⚠️ Not enough numeric columns for visualization.")

        # File Conversion Options
        st.subheader("🔄 Convert File")
        conversion_type = st.radio(f"Convert `{file.name}` to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"🎯 Convert `{file.name}` to {conversion_type}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                new_file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False)
                new_file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"📥 Download `{new_file_name}`",
                data=buffer,
                file_name=new_file_name,
                mime=mime_type,
            )

# Sidebar Completion Message
st.sidebar.success("✨All files processed successfully!")
