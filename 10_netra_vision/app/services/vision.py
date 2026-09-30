from google import genai
from dotenv import load_dotenv
load_dotenv()
import base64
import json

client = genai.Client()

CROP_ANALYSIS_PROMPT = """
    You are an expert agricultural scientist specializing in crop disease detection.
Analyze this image of a crop/plant and provide a detailed disease assessment.

Provide your analysis as a JSON object with exactly this structure:

{
"crop_detected": "Name of the crop or plant visible in the image",
"severity": "healthy" or "mild" or "moderate" or "severe" or "critical",
"diseases": [
        {
            "name": "Disease name",
            "confidence": 0.0 to 1.0,
            "description": "Brief description of the disease and visible symptoms"
        }
    ],
"treatments": [
        {
            "treatment_name": "Name of treatment",
            "treatment_type": "organic" or "chemical" or "preventive",
            "instructions": "Step by step treatment instructions",
            "urgency": "immediate" or "within_week" or "seasonal"
        }
    ],
    "overall_health": "One sentence summary of plant health",
    "additional_notes": "Any other observations or recommendations"
}
"""

def parse_analysis_response(output_text: str) -> dict:
    """Parse JSON returned by Gemini, including fenced or quoted JSON."""
    if not output_text or not output_text.strip():
        raise ValueError("Gemini returned an empty analysis response")

    text = output_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end <= start:
            raise ValueError("Gemini returned a response that is not valid JSON")
        result = json.loads(text[start:end + 1])

    if isinstance(result, str):
        result = json.loads(result)
    if not isinstance(result, dict):
        raise ValueError("Gemini analysis response must be a JSON object")
    return result


async def analyse_image(image_path:str, content_type: str):
    '''Analyse image content using Google Gemini'''

    def encode_image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")    
            return encoded_string
         
    base64_image = encode_image_to_base64(image_path)
    interactions = client.interactions.create(
        model="gemini-3.5-flash",
        input=[
            {"type":"text","text":CROP_ANALYSIS_PROMPT},
            {
                "type":"image",
                "data": base64_image,
                "mime_type":content_type
            }
        ]
    )
    return parse_analysis_response(interactions.output_text)


