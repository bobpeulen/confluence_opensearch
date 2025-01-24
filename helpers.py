## Supporting functions
from atlassian import Confluence
from bs4 import BeautifulSoup
import datetime
from datetime import datetime
import tiktoken
#from opensearchpy import OpenSearch, RequestsHttpConnection
from langchain.vectorstores import OpenSearchVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings
import oci
import ads
from tqdm import tqdm

def create_confluence_client(full_confluence_url, username_confluence, atlassian_api_token):

    confluence_client = Confluence(
        url=full_confluence_url,
        username=username_confluence,
        password=atlassian_api_token,
        cloud=True)

    return confluence_client


# def create_opensearch_client(host, username, password):

#     oci_opensearch_client = OpenSearch(
#         hosts=[{'host': host, 'port': 9200}],
#         http_auth=(username, password),
#         use_ssl=True,
#         verify_certs=False,
#         connection_class=RequestsHttpConnection)
    
#     return oci_opensearch_client

def create_opensearch_client(host, username, password, index_name, embedding_model):
    
    # Setup Resource Principal for authentication
    auth_provider = ads.set_auth("api_key", oci_config_location = "/home/datascience/.oci/config")
    auth = (username, password)
    AUTH_TYPE = "API_KEY"

    # Initialize OpenSearch as the vector database
    oci_opensearch_client = OpenSearchVectorSearch(opensearch_url=host, 
                                index_name=index_name, 
                                embedding_function=embedding_model,
                                signer=auth_provider,
                                auth_type=AUTH_TYPE,
                                http_auth=auth)
    
    return oci_opensearch_client




def create_embedding_model():
    
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")
    
    return embedding_model



def ingest_documents_with_embeddings(chunks, index_name, oci_opensearch_client, host, username, password, embedding_model, batch_size=100):

    print(f"Index Name: {index_name}")
    
    auth = (username, password)
    
    # Ingest documents in batches
    for i in tqdm(range(0, len(chunks), batch_size), desc="Ingesting batches"):
        batch = chunks[i:i + batch_size]
        try:
            oci_opensearch_client.add_texts(texts=batch, 
                     bulk_size=batch_size,
                     embedding=embedding_model, 
                     host=host, 
                     index_name=index_name,
                     http_auth=auth)
        except Exception as e:
            print(f"Error while adding texts to the opensearch {index_name} index. Error occured in chunks batch {i + 1}-{i+batch_size}: {e}")
    
    #refresh index
    oci_opensearch_client.client.indices.refresh(index=index_name)
    print(f"Index '{index_name}' refreshed!")
    print(f"Successfully ingested {len(chunks)} documents into the OpenSearch index '{index_name}'!")






def chunk_text(output_text, max_tokens):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(output_text)

    chunks = []
    current_chunk = []
    current_length = 0

    for token in tokens:
        if current_length + 1 <= max_tokens:
            current_chunk.append(token)
            current_length += 1
        else:
            # Finalize the current chunk and start a new one
            chunk_text = encoding.decode(current_chunk)
            chunks.append(chunk_text)
            current_chunk = [token]
            current_length = 1

    
    if current_chunk:
        chunk_text = encoding.decode(current_chunk)
        chunks.append(chunk_text)

    return chunks





def parse_page(confluence_client, page_id):
    
    #################################################################### Get the body of the page
    ####################################################################
    
    #get the full page
    result_one_page = confluence_client.get_page_by_id(page_id, expand="body.storage")

    #get html body
    html_body = result_one_page['body']['storage']['value']

    #parse html page into text
    soup = BeautifulSoup(html_body, features="html.parser")

    # kill all script and style elements from the body
    for script in soup(["script", "style"]):
        script.extract() 

    # get text
    output_text = soup.get_text()
    
    #apply chunking the text
    chunks = chunk_text(output_text, max_tokens=400)
    
    return chunks
