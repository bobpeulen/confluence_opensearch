# Confluence Trigger to Automate Vectorizing

- Confluence will trigger when a page has been edited, a HTTP request will be send to API Gateway/OCI Functions
- OCI Functions will either write to OCI Streaming/Data Prepper/OCI OCI OpenSearch or directly apply logic

**Steps**

1. Create an API Gateway and deployment
2. Create Automation rule in Confluence using the API Gateway endpoint
3. Create OCI OpenSearch Clusters. Set up embedding model, conversation history, GenAI connection
   Use: https://github.com/bobpeulen/oci_opensearch/blob/main/oci_opensearch_rag_auto.ipynb
4. Create OCI Functions deployment

# OCI Functions

- log in Docker
  ```
  docker login -u '[namespace]/OracleIdentityCloudService/bob.peulen@oracle.com' iad.ocir.io
  password = Auth token
  ```
  
- Create function
  ```
  fn init --runtime python confluencex
  cd confluencex
  ```

  - Invoke
    ```
    fn invoke app_bp confluencex
    ```

- Change func.py



![image](https://github.com/user-attachments/assets/aa232819-0666-4445-b7ef-e8c9f8b5f2b2)
