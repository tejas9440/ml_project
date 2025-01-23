import streamlit as st
import pandas as pd

# Load the pickle file
file_path = './popular.pkl'
data = pd.read_pickle(file_path)

# Unpack data
book_name = data['Book-Title'] if 'Book-Title' in data.columns else ["Book 1", "Book 2"]
author = data['Book-Author'] if 'Book-Author' in data.columns else ["Author 1", "Author 2"]
votes = data['Num_Ratings'] if 'Num_Ratings' in data.columns else [100, 200]
rating = data['AVG_Ratings'] if 'AVG_Ratings' in data.columns else [4.5, 4.7]
image = data['Image-URL-M'] if 'Image-URL-M' in data.columns else [
    "https://via.placeholder.com/200",
    "https://via.placeholder.com/200",
]

# Streamlit page configuration
st.set_page_config(page_title="Book Recommendation System", layout="wide")

# Navbar for navigation
st.markdown(
    """
    <style>
    .navbar {
        display: flex;
        justify-content: center;
        background-color: #f8f9fa;
        padding: 10px 0;
        border-bottom: 1px solid #ddd;
    }
    .navbar a {
        text-decoration: none;
        color: #007bff;
        font-weight: bold;
        padding: 0 15px;
    }
    .navbar a:hover {
        color: #0056b3;
    }
    .navbar a.active {
        color: #0056b3;
        border-bottom: 2px solid #007bff;
    }
    </style>
    <div class="navbar">
        <a href="#" id="home-tab" class="active" onclick="window.location.hash='home';">Home</a>
        <a href="#" id="search-tab" onclick="window.location.hash='search';">Search</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Handle navigation between Home and Search tabs
# Handle navigation between Home and Search tabs
if "page" not in st.session_state:
    st.session_state.page = "home"  # Default page

# Update page state based on user interaction
if "hash" in st.query_params:
    st.session_state.page = st.query_params.get("hash")[0]

# Logic for rendering pages
if st.session_state.page == "home":
    # Home Page
    st.title("📚 Book Recommendation System")
    st.markdown("### Explore the top 50 books based on ratings and reviews.")

    # Display books in a grid layout
    cols_per_row = 4  # Number of cards per row
    for i in range(0, len(book_name), cols_per_row):
        cols = st.columns(cols_per_row)
        for col, idx in zip(cols, range(i, min(i + cols_per_row, len(book_name)))):
            with col:
                st.image(image[idx], use_container_width=True, caption=book_name[idx])
                st.markdown(f"**Author:** {author[idx]}")
                st.markdown(f"**Votes:** {votes[idx]} | **Rating:** {rating[idx]}")
                st.button("Learn More", key=f"button_{idx}")

elif st.session_state.page == "search":
    # Search Page
    st.title("🔍 Search Books")
    st.markdown("### Find your next favorite book by searching below.")

    # Search input and button
    search_query = st.text_input("Enter book title or author:")
    if st.button("Search"):
        # Display results (placeholder logic for now)
        st.markdown(f"#### Results for '{search_query}':")
        # Filter data based on search (if applicable)
        results = data[data['Book-Title'].str.contains(search_query, case=False, na=False) |
                       data['Book-Author'].str.contains(search_query, case=False, na=False)]
        if not results.empty:
            for _, row in results.iterrows():
                st.image(row['Image-URL-M'], width=100)
                st.markdown(f"**{row['Book-Title']}** by {row['Book-Author']}")
                st.markdown(f"**Votes:** {row['Num_Ratings']} | **Rating:** {row['AVG_Ratings']}")
        else:
            st.write("No results found.")
