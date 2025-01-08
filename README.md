# Confluence Trigger to Automate Vectorizing

- Confluence will trigger when a page has been edited, a HTTP request will be send to API Gateway/OCI Functions
- OCI Functions will either write to OCI Streaming/Data Prepper/OCI OCI OpenSearch or directly apply logic

**Steps**

1. Create an API Gateway and deployment
2. Create Automation rule in Confluence using the API Gateway endpoint
3. Create OCI OpenSearch Clusters. Set up embedding model, conversation history, GenAI connection
   Use: https://github.com/bobpeulen/oci_opensearch/blob/main/oci_opensearch_rag_auto.ipynb
4. Create OCI Functions deployment

# API Gateway
- Create an API Gateway and deployment with PUT/POST. In this example, we use "confluence" and "updatepage" as paths.
- This example used no authentication, but you might add. 

# Create Confluence automation rule
- Add the API Gateway deployment full path in rule

   ```
  {
   "page_id":"{{pageidsmart}}",
   "page_url":"{{pageurlsmart}}"
   }
   ```

![image](https://github.com/user-attachments/assets/aa232819-0666-4445-b7ef-e8c9f8b5f2b2)

# OCI OpenSearch
- Create an OCI OpenSearch cluster
- Create a OCI Data Science notebook in same VCN, private subnet + NAT gateway
- Follow these steps: https://github.com/bobpeulen/oci_opensearch/blob/main/oci_opensearch_rag_auto.ipynb

# OCI Functions

- Create repo/project and log in Docker
  ```
  docker login -u '[namespace]/OracleIdentityCloudService/bob.peulen@oracle.com' iad.ocir.io
  password = Auth token
  ```
  
- Create function
  ```
  fn init --runtime python confluencex
  cd confluencex
  ```
- Change the func.py and requirements.txt

- Test function. Deploy and invoke function. Default values should be printed (in logs) and returned.
  ```
  fn -v deploy --app app_bp
  fn invoke app_bp confluencex
  ```





