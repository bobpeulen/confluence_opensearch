## Supporting functions
from atlassian import Confluence
from bs4 import BeautifulSoup
import datetime
from datetime import datetime
import tiktoken
from opensearchpy import OpenSearch, RequestsHttpConnection

def create_confluence_client(full_confluence_url, username_confluence, atlassian_api_token):

    confluence_client = Confluence(
        url=full_confluence_url,
        username=username_confluence,
        password=atlassian_api_token,
        cloud=True)

    return confluence_client




def create_opensearch_client(host, username, password):

    oci_opensearch_client = OpenSearch(
        hosts=[{'host': host, 'port': 9200}],
        http_auth=(username, password),
        use_ssl=True,
        verify_certs=False,
        connection_class=RequestsHttpConnection)
    
    return oci_opensearch_client




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
