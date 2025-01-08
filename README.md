# Confluence Trigger to Automate Vectorizing

- Confluence will trigger when a page has been edited, a HTTP request will be send to API Gateway/OCI Functions
- OCI Functions will either write to OCI Streaming/Data Prepper/OCI OCI OpenSearch or directly apply logic


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
