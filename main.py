from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
import httpx
import json

app = FastAPI(
    title="Qwen3 FastAPI Proxy",
    description="A proxy API to connect to an OpenAI-compatible model service like LM Studio.",
    version="1.2.0"
)

# LM Studio API endpoint running on the host machine
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

async def stream_generator(request, request_data):
    """Generator for streaming responses from LM Studio."""
    async with httpx.AsyncClient() as client:
        try:
            async with client.stream(
                "POST",
                LM_STUDIO_URL,
                json=request_data,
                headers={key: value for key, value in request.headers.items() if key.lower() not in ['host', 'content-length', 'accept-encoding']},
                timeout=120
            ) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes():
                    yield chunk
        except Exception as e:
            print(f"An error occurred during streaming: {e}")
        # Yielding an error message in the stream is complex, so we log for now.
        # The client will likely experience a dropped connection.

@app.post("/v1/chat/completions")
async def chat_proxy(request: Request):
    """
    Acts as a proxy, forwarding requests to the LM Studio server.
    Supports both streaming and non-streaming responses.
    """
    request_data = await request.json()
    is_streaming = request_data.get("stream", False)

    if is_streaming:
        return StreamingResponse(
            stream_generator(request, request_data),
            media_type="text/event-stream"
        )
    else:
        # Handle non-streaming requests
        async with httpx.AsyncClient() as client:
            # Handle non-streaming requests
            lm_studio_response = None
            try:
                lm_studio_response = await client.post(
                    LM_STUDIO_URL,
                    json=request_data,
                    headers={key: value for key, value in request.headers.items() if key.lower() not in ['host', 'content-length']},
                    timeout=120
                )
                lm_studio_response.raise_for_status()
                response_data = lm_studio_response.json()
                return JSONResponse(content=response_data, status_code=lm_studio_response.status_code)

            except httpx.RequestError as e:
                print(f"Error connecting to LM Studio: {e}")
                raise HTTPException(status_code=502, detail=f"Error connecting to LM Studio: {e}")
            except json.JSONDecodeError:
                error_message = f"LM Studio returned non-JSON response. Status: {lm_studio_response.status_code}. Content: {lm_studio_response.text[:500]}..."
                print(error_message)
                raise HTTPException(status_code=500, detail=error_message)
            except Exception as e:
                error_detail = f"An unexpected error occurred in proxy: {e}"
                raw_response_text = "N/A"
                if lm_studio_response is not None and hasattr(lm_studio_response, 'text'):
                    raw_response_text = lm_studio_response.text[:500] + "..."
                print(f"{error_detail}. LM Studio raw response (if available): {raw_response_text}")
                raise HTTPException(status_code=500, detail=error_detail)

@app.get("/")
def read_root():
    return {"message": "Qwen3 FastAPI Proxy is running. Use the /v1/chat/completions endpoint to interact with the model."}
