import streamlit as st
from scraper import (
    scrape_website, 
    extract_body_content, 
    clean_extracted_body, 
    chunk_dom_content
)
from parser import parse_w_ollama

st.title("AI Web Scraper")
url = st.text_input("Enter a Website Url")  

if st.button("Scrape Site"):
    st.write("Scraping the Website")

    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_extracted_body(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)


if "dom_content" in st.session_state:
    parse_desc = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_desc:
            st.write("Parsing the content")

            dom_chunks = chunk_dom_content(st.session_state.dom_content)
            result = parse_w_ollama(dom_chunks, parse_desc)
            st.write(result)


