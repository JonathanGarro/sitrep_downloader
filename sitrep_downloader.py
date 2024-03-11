import streamlit as st
import requests
import csv

def get_go_docs(event_id):
    url = f"https://goadmin.ifrc.org/api/v2/situation_report/?event={event_id}"
    result_list = []
    page_count = 0
    page_limit = 10  # set a page limit if looking at big event
    
    while url and page_count < page_limit:
        response = requests.get(url)
        data = response.json()
        results = data.get("results", [])
    
        for result in results:
            temp_dict = {}
            temp_dict['doc_name'] = result['name']
            
            # doc_url is stored either in 'document' or 'document_url' key
            if 'document' in result and result['document']:
                temp_dict['doc_url'] = result['document']
            else:
                temp_dict['doc_url'] = result.get('document_url', '')
                
            # check for nested 'type' key
            if 'type' in result and 'type' in result['type']:
                temp_dict['nested_type'] = result['type']['type']
            else:
                temp_dict['nested_type'] = None
                
            result_list.append(temp_dict)
            print(result)
        
        url = data.get("next")
        page_count += 1
    
    keys = result_list[0].keys()
    with open("output.csv", "w", newline="") as a_file:
        dict_writer = csv.DictWriter(a_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(result_list)

st.title("IFRC API Data Retrieval")

id_to_search = st.number_input("Enter Event ID to Search", value=5027, step=1)

if st.button("Retrieve Data"):
    get_go_docs(id_to_search)
    st.success("Data retrieved successfully!")

