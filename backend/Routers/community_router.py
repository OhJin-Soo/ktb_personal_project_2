from fastapi import APIRouter, Form, HTTPException
from Controllers.community_controller import predict_image
from Schemas.community_schemas import InferenceResponse

router = APIRouter(prefix="/community", tags=["Community"])

@router.post("/infer", response_model=InferenceResponse)
async def infer_image(image_base64: str = Form(...)):
    """
    Perform ResNet18 inference on uploaded image.
    
    Args:
        image_base64: Base64 encoded image string
        
    Returns:
        Inference results with status, probabilities, and risk score
    """
    try:
        result = predict_image(image_base64)
        return InferenceResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")

