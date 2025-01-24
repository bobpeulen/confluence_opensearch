
import io
import json
from fdk import response
from atlassian import Confluence
from bs4 import BeautifulSoup
import datetime
from datetime import datetime
import tiktoken
from langchain.vectorstores import OpenSearchVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings
import oci
import ads
from tqdm import tqdm

#load configuration
from config import confluence_space_id, full_confluence_url, username_confluence, atlassian_api_token, host, username, password, index_name

#Load all customer functions
from helpers import create_embedding_model
from helpers import ingest_documents_with_embeddings
from helpers import chunk_text
from helpers import parse_page
from helpers import create_confluence_client
from helpers import create_opensearch_client


def handler(ctx, data: io.BytesIO=None):
    
    page_id = "no_page_id_available"
    page_url = "no_page_url_available"

    try:
        
        ## establish connections
        confluence_client = create_confluence_client(full_confluence_url, username_confluence, atlassian_api_token)
        oci_opensearch_client = create_opensearch_client(host, username, password)
        
        #get the body and values
        body = json.loads(data.getvalue())
        print(f"Printing the body {body}")
        page_id = body.get("page_id")
        page_url = body.get("page_url")
        print(f"Printing the page_id {page_id}")
        print(f"Printing the page_url {page_url}")
        
        # parse the page and create chunks
        chunks = parse_page(confluence_client, page_id)
        
        #parse chunks of text into embeddings
        embedding_model = create_embedding_model()
        
        # convert chunks into embeddings and push to OCI OpenSearch.
        ingest_documents_with_embeddings(chunks=chunks, index_name=index_name, oci_opensearch_client=oci_opensearch_client, host=host, username=username, password=password, embedding_model=embedding_model, batch_size=5)
        
    except (Exception, ValueError) as ex:
        print(str(ex), flush=True)
        print("Not loaded any data")

    return response.Response(
        ctx, response_data=json.dumps(
            {"message": "The changed page id is {0}".format(page_id)}),
        headers={"Content-Type": "application/json"}
    )
