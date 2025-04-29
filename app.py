  import streamlit as st
  import chromadb
  from streamlit_extras.add_vertical_space import add_vertical_space

  # Set page config for dark theme
  st.set_page_config(
      page_title="VSearch",
      page_icon="🔍",
      layout="centered",
      initial_sidebar_state="expanded"
  )

  # Custom CSS for dark mode styling
  st.markdown("""
      <style>
      .stApp {
          background-color: #1E1E1E;
          color: #FFFFFF;
      }
      .stTextInput>div>div {
          background-color: transparent !important;
      }
      .stButton>button {
          background-color: #7C3AED;
          color: #FFFFFF;
          border-radius: 8px;
          padding: 0.5rem 2rem;
          border: none;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
      }
      .stButton>button:hover {
          background-color: #6D28D9;
          border: none;
      }
      a {
          color: #7C3AED !important;
          text-decoration: underline !important;
          pointer-events: auto !important;
          cursor: pointer !important;
      }
      </style>
      """, unsafe_allow_html=True)

  # Header with custom styling
  st.markdown("<h1 style='text-align: center; color: #7C3AED; margin-bottom: 2rem;'>VSearch</h1>", unsafe_allow_html=True)

  add_vertical_space(2)

  # Search input with placeholder
  q = st.text_input(
      "Enter your search query",
      placeholder="Type your search query here...",
      help="Enter keywords to search through the vector database"
  )

  # Search button
  if st.button("🔍 Search", use_container_width=True):
      if q:
          try:
              with st.spinner('Searching...'):
                  # Connect to ChromaDB persistent client
                  chroma_client = chromadb.PersistentClient(path="vectordb")
                
                  # Try to get collection
                  collection = chroma_client.get_collection(name="search0_collection")
                
                  # Query the collection
                  results = collection.query(
                      query_texts=[q],
                      n_results=3,
                      include=["documents", "metadatas"]
                  )
                
                  # Display results in cards
                  for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
                      # Convert URLs to clickable links with explicit onclick
                      import re
                      url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                      doc_with_links = re.sub(url_pattern, lambda x: f'<a href="{x.group()}" target="_blank" onclick="window.open(\'{x.group()}\', \'_blank\')">{x.group()}</a>', doc)
                      
                      # Convert metadata URLs to clickable links
                      metadata_str = str(metadata)
                      metadata_with_links = re.sub(url_pattern, lambda x: f'<a href="{x.group()}" target="_blank" onclick="window.open(\'{x.group()}\', \'_blank\')">{x.group()}</a>', metadata_str)
                    
                      st.markdown(f"""
                          <div style='
                              background-color: #2D2D2D;
                              padding: 1.5rem;
                              border-radius: 10px;
                              margin: 1rem 0;
                              border-left: 4px solid #7C3AED;
                          '>
                              <p style='color: #FFFFFF;'>{doc_with_links}</p>
                              <p style='color: #9CA3AF; font-size: 0.875rem;'>Metadata: {metadata_with_links}</p>
                          </div>
                          """, unsafe_allow_html=True)
                        
          except Exception as e:
              st.error(f"An error occurred: {str(e)}")
      else:
          st.warning("⚠️ Please enter a search query.")

  add_vertical_space(2)

  # Footer
  st.markdown("""
      <div style='text-align: center; color: #9CA3AF; padding: 2rem;'>
          Powered by ChromaDB and Streamlit
      </div>
      """, unsafe_allow_html=True)