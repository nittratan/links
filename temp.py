from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from rabbitmq_publisher import publish_message_to_queue
from utils.auth import authenticate_request
from utils.logger import log_request
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class JobTriggerRequest(BaseModel):
    job_name: str


@router.post("/batch-trigger", summary="Trigger batch job manually", tags=["Batch Jobs"])
@log_request
@authenticate_request
async def trigger_batch_job(request: Request):
    """
    Publishes a manual batch job trigger message to RabbitMQ.
    
    ### Request:
    - **Method**: POST  
    - **Headers**: `Content-Type: application/json`  
    - **Body**:  
        - `job_name` (str, required): Name of the batch job to trigger.

    ### Response:
    - **200 OK**: Message successfully published.
    - **400 Bad Request**: Invalid payload.
    - **500 Internal Server Error**: Failure in publishing message.
    """
    try:
        payload = await request.json()
        job_name = payload.get("job_name")
        if not job_name:
            raise ValueError("Missing 'job_name' in payload")

        logger.info(
            msg={
                "message": "Batch job trigger request received.",
                "job_name": job_name
            },
            extra={"source": "CCA Test", "target": "RabbitMQ"},
        )

        pub_msg = {
            "trigger": job_name,
            "message": {"job_name": job_name}
        }

        response = await publish_message_to_queue(pub_msg)
        if response.get("status") != "success":
            raise Exception(f"Failed to publish: {response.get('message')}")

        return JSONResponse(
            content={"success": True, "message": "Batch job trigger published."},
            status_code=200
        )

    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        return JSONResponse(
            content={"success": False, "message": str(ve)},
            status_code=400
        )
    except Exception as e:
        logger.error(f"Exception while publishing batch trigger: {str(e)}")
        return JSONResponse(
            content={"success": False, "message": "Internal server error", "details": str(e)},
            status_code=500
        )



{
  "job_name": "daily_adjustments"
}



from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from rabbitmq_publisher import publish_message_to_queue
from utils.auth import authenticate_request
from utils.logger import log_request
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/batch-trigger", summary="Trigger batch job manually", tags=["Batch Jobs"])
@log_request
@authenticate_request
async def trigger_batch_job(request: Request):
    """
    Triggers a batch job by publishing a message to RabbitMQ.

    ### Request:
    - **Method**: POST  
    - **Headers**: `Content-Type: application/json`  
    - **Body**:  
        - `job_name` (str, required)

    ### Response:
    - **200 OK**: Message successfully published.
    - **400 Bad Request**: Invalid payload.
    - **500 Internal Server Error**: Message publishing failed.
    """
    try:
        payload = await request.json()
        job_name = payload.get("job_name")

        if not job_name:
            raise ValueError("Missing 'job_name' in request payload")

        logger.info(
            msg={
                "message": "Batch job trigger request received.",
                "job_name": job_name
            },
            extra={"source": "CCA Test", "target": "RabbitMQ"},
        )

        pub_msg = {
            "trigger": job_name,
            "message": {"job_name": job_name}
        }

        response = await publish_message_to_queue(pub_msg)
        if response.get("status") != "success":
            raise Exception(f"RabbitMQ publish failed: {response.get('message')}")

        return JSONResponse(
            content={"success": True, "message": "Batch job trigger published successfully."},
            status_code=200
        )

    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        return JSONResponse(
            content={"success": False, "message": str(ve)},
            status_code=400
        )

    except Exception as e:
        logger.error(f"Internal server error: {str(e)}")
        return JSONResponse(
            content={"success": False, "message": "Internal Server Error", "details": str(e)},
            status_code=500
        )

