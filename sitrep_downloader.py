import streamlit as st
import requests
import csv
import io

def get_go_docs(event_id):
    url = f"https://goadmin.ifrc.org/api/v2/situation_report/?event={event_id}"
    result_list = []
    page_count = 0
    page_limit = 10  # set a page limit if looking at a big event
    
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
    
    # create a CSV file in memory
    csv_data = io.StringIO()
    keys = result_list[0].keys()
    dict_writer = csv.DictWriter(csv_data, keys)
    dict_writer.writeheader()
    dict_writer.writerows(result_list)
    
    return csv_data.getvalue()

st.title("IFRC API - Retrieve SitReps by Event")

id_to_search = st.number_input("Enter Event ID to Search", value=5027, step=1)

# button to trigger data retrieval and download CSV file
if st.button("Retrieve Data"):
    csv_data = get_go_docs(id_to_search)
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="output.csv",
        mime="text/csv"
    )
    st.success("Data retrieved successfully!")
