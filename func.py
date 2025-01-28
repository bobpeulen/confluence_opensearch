import io
import json
import logging
import oci
import requests
from fdk import response


def handler(ctx, data: io.BytesIO = None):
    auth = oci.auth.signers.get_resource_principals_signer()
    logger = logging.getLogger()
    try:
        logger.info("Inside function")
        body = json.loads(data.getvalue())
        logger.info("Body : " + json.dumps(body))
        headers = ctx.Headers()
        logger.info("Headers: " + json.dumps(headers))

        #get http endpoint from body        
        endpoint = body.get("model_deployment_http_endpoint")

        #send the full body
        resp = requests.post(endpoint, json=body, auth=auth)
        logger.info("response : " + resp.json())
    except (Exception, ValueError) as ex:
        logger.error("Failed to call endpoint with ex : {}".format(str(ex)))
    return response.Response(
            ctx, response_data=resp.json(),
            headers={"Content-Type": "application/json"}
        )
