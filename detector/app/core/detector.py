import logging
import torch

async def predict_and_detect(chosen_model, img, class_name='person', conf=0.5, rectangle_thickness=2, text_thickness=1):
    """
    Asynchronously performs object detection on the given image using the specified model.
    Args:
        chosen_model: The pre-trained model to use for object detection. 
                      It should have a `predict` method and a `names` attribute mapping class indices to class names.
        img: The input image to perform detection on. It can be in a format supported by the model.
        class_name (str, optional): The name of the class to detect. Defaults to 'person'.
        conf (float, optional): The confidence threshold for predictions. Defaults to 0.5.
        rectangle_thickness (int, optional): The thickness of the rectangle drawn around detected objects. Defaults to 2.
        text_thickness (int, optional): The thickness of the text displayed on detected objects. Defaults to 1.
    Returns:
        results: The detection results from the model, which may include bounding boxes, confidence scores, 
                 and other information depending on the model's implementation.
    """
    logger = logging.getLogger(__name__)
    
    # Get the class index for 'person'
    class_index = list(chosen_model.names.values()).index(class_name)
    
    # Ensure the model is explicitly set to GPU mode if available
    try:
        # Check if GPU is available and set the device accordingly
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        # Perform prediction with the appropriate device
        results = chosen_model.predict(img, classes=[class_index], conf=conf, device=device)
        logger.info(f"Detection completed using {device.upper()}")
        
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        # Re-raise with more context
        raise RuntimeError(f"Model inference failed: {str(e)}")
    
    return results
