import requests
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# YouTrack API Configuration
YOU_TRACK_URL = "https://s2py.youtrack.cloud/api"
API_TOKEN = "perm:U2hhc2hhbmtfWWFra2FudGk=.NDctMg==.v2W9i1Hg2ZFpBbGCmUu0LIbSvgxKNL"
PROJECT_ID = "112"  # Replace with your project ID

# Headers for API Authentication
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json"
}

# Function to fetch issues from YouTrack
def fetch_issues(project_id):
    url = f"{YOU_TRACK_URL}/issues"
    params = {
        "query": f"project: {project_id}",
        "fields": "idReadable,summary,customFields(name,value(name))"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    
    if response.status_code == 200:
        issues = response.json()
        return issues
    else:
        print(f"Failed to fetch issues: {response.status_code}, {response.text}")
        return []

# Function to calculate project progress
def calculate_progress(issues):
    total_issues = len(issues)
    Submitted_count = 0
    git_uploaded = 0
    
    for issue in issues:
        # Check the "state" and "Git Uploaded" fields in customFields
        for field in issue.get("customFields", []):
            if field.get("name") == "State":  # Ensure the field is the "State"
                state_value = field.get("value", {}).get("name")
                if state_value == "Submitted":
                    Submitted_count += 1
            
            if field.get("name") == "Git Uploaded":  # Check for "Git Uploaded"
                git_uploaded_value = field.get("value", {}).get("name")
                if git_uploaded_value == "Yes":
                    git_uploaded += 1
    
    return total_issues, Submitted_count, git_uploaded


# Function to generate graphs for project progress
def generate_graphs(total_issues, Submitted_issues, git_uploaded):
    # Prepare data for graph
    labels = ["Submitted", "Git Uploaded", "In Progress"]
    values = [Submitted_issues, git_uploaded, total_issues - Submitted_issues]

    # Plot bar chart for project progress
    plt.figure(figsize=(10, 6))
    sns.barplot(x=labels, y=values, palette="Blues_d")  # Removed 'hue' parameter
    plt.title("Project Progress", fontsize=16)
    plt.xlabel("Status", fontsize=12)
    plt.ylabel("Number of Issues", fontsize=12)
    plt.legend(title='Status', loc='upper right', labels=labels)  # Adding legend for clarity
    st.pyplot(plt)  # Streamlit specific function to render the plot


# Streamlit UI
def main():
    # Display title in Streamlit
    st.title("YouTrack Project Progress Dashboard")

    # Fetch issues and calculate progress
    issues = fetch_issues(PROJECT_ID)
    total_issues, Submitted_issues, git_uploaded = calculate_progress(issues)

    # Display metrics in Streamlit
    st.subheader("Project Progress Metrics")
    st.write(f"Total Issues: {total_issues}")
    st.write(f"Development Submitted: {Submitted_issues}")
    st.write(f"Git Uploaded: {git_uploaded}")
    
    if total_issues - Submitted_issues > 0:
        st.write(f"In Progress Issues: {total_issues - Submitted_issues}")
    else:
        st.write("All issues are Submitted!")

    # Generate and display graphs
    generate_graphs(total_issues, Submitted_issues, git_uploaded)

# Run the Streamlit app
if __name__ == "__main__":
    main()
