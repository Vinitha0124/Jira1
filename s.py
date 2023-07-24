import streamlit as st #Used for Frontend
import requests #used for sending request
from requests.auth import HTTPBasicAuth  #for authentication purpose
import json #note: this is just used to only format json file while diplaying not for api call


#demo_function will perform operations using my credentials
#one can just get all projects, get a single project and delete the project

    

def Demo_function(project_id, op, project_name):
    email = "vvchow124@gmail.com"
    api_token = "ATATT3xFfGF01jyvzqioarDJXVjfwurJ0Hlo6jnmDURbNNspi1PBkNEdpKyPTLubyZtvf901_hxaoLDhqPF37aFIfOOlaS9zD5WJ6SSLYcrNVUoOS4XQrQZ9lmgQRKpKcHmHyDe0pX-so0zHtUHHyCjxkCM8Z_CW1vdh9tneg1qRqTow67rPpHg=B3E91EED"
    url = "https://vvchow.atlassian.net/rest/api/3/project"
   
    try:
        auth = HTTPBasicAuth(email, api_token)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload_request = {}
        if project_id == "" and op == "GET":
            response = requests.get(url, headers=headers, auth=auth)

            if response.status_code == 200:
                results = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ":"))
                st.json(results)
            else:
                st.error(f"Error: Failed to fetch data. Status code: {response.status_code}")
            return
        
        # elif op == "POST":
        #     payload_request = create_or_update(project_id, project_name)
        #     new_url =  url
        # elif op == "PUT":
        #     payload_request = create_or_update(project_id, project_name)
        #     new_url = url + f"/{project_id}"

        else:
            new_url = url + f"/{project_id}"
        response = requests.request(
            op,
            new_url,
            data=payload_request if payload_request != {} else {},
            headers=headers,
            auth=auth
        )
        if str(response.status_code).startswith("2"):
            st.write("Successfully Executed: ", response.status_code)
            st.write(response.json())
        else:
            st.write("Check your credentials: ", response.status_code)
    except Exception as e:
        st.error(f"{e}")

def my_function():
    url = st.text_input("Base_URL")
    email = st.text_input("Email_ID")
    api_token = st.text_input("API Token", type="password")
    clicked = st.button("Enter")

    if clicked:
        auth = HTTPBasicAuth(email, api_token)

        headers = {
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers, auth=auth)

        if response.status_code == 200:
            st.write(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        else:
            st.error(f"Error: Failed to fetch data. Status code: {response.status_code}")

def main():
    st.title("Jira account management")
    st.markdown("### This page will give you about the info of your Jira projects")
    st.write("Choose your_credentials if you want to display all your Jira Projects else \n choose demo where you can see the information of a demo account")

    choice = st.radio("Choose any one", ["Your_credentials", "Demo"])
    project_name=""
    if choice == "Demo":
            project_id = ""
            op = "GET"
            crud = st.radio("RUD", ["Get a project", "Get all projects", "Delete the project"])
            # if crud == "Create a project":
            #     op = "POST"
            #     project_id = st.text_input("Enter project id:")
            #     project_name = st.text_input("Enter project name:")
            if crud == "Get a project":
                op = "GET"
                project_id = st.text_input("Enter project id:")
            # elif crud == "Update the project":
            #     op = "PUT"
            #     project_id = st.text_input("Enter project id:")
            #     project_id = st.text_input("Enter the project name you want to update:")
            elif crud == "Delete the project":
                op = "DELETE"
                project_id = st.text_input("Enter the project id")
            clicked = st.button("OPERATION", key=122)
            if clicked:
                Demo_function(project_id, op, project_name)
    elif choice == "Your_credentials":
        st.write("Results from your credentials:")
        my_function()



if __name__=="__main__":
    main()


    