from PIL import Image, ImageFile
from io import BytesIO
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18, ResNet18_Weights
import base64

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Model loading (singleton pattern - load once)
_device = None
_model = None
_class_names = None

def get_model():
    """Lazy load the model on first use"""
    global _device, _model, _class_names
    
    if _model is None:
        _device = torch.device("cpu")
        _model = resnet18(weights=ResNet18_Weights.DEFAULT)
        _model.fc = torch.nn.Linear(512, 3)  # 3 classes
        _model.to(_device)
        _model.eval()
        _class_names = ["good", "bad", "risk"]
    
    return _model, _device, _class_names

def preprocess_image(image: Image.Image):
    """Preprocess image for model input"""
    transform = transforms.Compose([
        transforms.Resize((300, 300)),
        transforms.CenterCrop(256),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

def predict_image(image_base64: str) -> dict:
    """
    Perform inference on base64 encoded image.
    
    Args:
        image_base64: Base64 encoded image string
        
    Returns:
        Dictionary with prediction results
    """
    try:
        # Decode base64 to PIL Image
        image = Image.open(BytesIO(base64.b64decode(image_base64))).convert('RGB')
    except Exception as e:
        raise ValueError(f"Invalid image input: {str(e)}")
    
    # Get model
    model, device, class_names = get_model()
    
    # Preprocess and predict
    input_tensor = preprocess_image(image).to(device)
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        predicted_class_idx = torch.argmax(probabilities).item()
        predicted_class = class_names[predicted_class_idx]
        risk = torch.sum(probabilities * torch.tensor([1.0, 0.0, 0.5], device=device)).item()
    
    # Return results
    return {
        "status": predicted_class,
        "probabilities": probabilities.tolist(),
        "risk_score": float(risk),
        "predicted_class_index": int(predicted_class_idx)
    }

