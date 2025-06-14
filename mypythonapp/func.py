import io
import json
import logging

from fdk import response


def handler(ctx, data: io.BytesIO = None):
    logging.getLogger().info("Inside Python Hello World function - Simplified")
    return response.Response(
        ctx, response_data=json.dumps(
            {"message": "Hello World from Simplified Function"}),
        headers={"Content-Type": "application/json"}
    )
