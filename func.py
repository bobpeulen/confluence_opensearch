import io
import json
from fdk import response

#custom
from atlassian import Confluence
from bs4 import BeautifulSoup
import datetime
from datetime import datetime
import tiktoken
from transformers import BertTokenizer, BertModel
import torch
from opensearchpy import OpenSearch, RequestsHttpConnection

from config import confluence_space_id, full_confluence_url, username_confluence, atlassian_api_token, host, username, password
from helpers import create_confluence_client, create_opensearch_client, chunk_text, parse_page

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
        
        # push chunks to OCI OpenSearch.
        
        
        
        
    except (Exception, ValueError) as ex:
        print(str(ex), flush=True)
        print("Not loaded any data")

    return response.Response(
        ctx, response_data=json.dumps(
            {"message": "The changed page id is {0}".format(page_id)}),
        headers={"Content-Type": "application/json"}
    )
