import os
from dotenv import load_dotenv
from flask_restx import Namespace

load_dotenv()

#Fields
available_fields = {
    "name": "Name",
    "location": "Location",
    "details": "Details",
    "image": "Image",
    "population": "Population",
    "latitude": "Latitude",
    "longitude": "Longitude"
}

valid_fields = {
    "Name",
    "Location",
    "Details",
    "Image",
    "Population",
    "Latitude",
    "Longitude"
}

#Patterns
words_pattern = r'with:\s*(.*?)(?:\b(?:ascending|descending|return|show|sort|by)\b|[.!?]|$)'
separators_pattern = r'\b(?:and|or)\b|,'
response_pattern = r"^```[a-z]*\n"

#ENV
Monkeys_Url = os.getenv("MONKEYS_URL")
Gemini_Key = os.getenv("GEMINI_KEY")
Gemini_Api_Url = os.getenv("GEMINI_API_URL")

#Swagger
Swagger_Version = os.getenv('VERSION')
Swagger_Title = os.getenv('TITLE')
Swagger_Description = os.getenv('DESCRIPTION')
Swagger_Doc = os.getenv('DOC')
Swagger_Prefix = os.getenv('PREFIX')
CACHE_EXPIRATION_TIME=30

#Namespaces
MCP_NS = Namespace('mcp', description='MCP (Model Context Protocol) operations')
CHAT_NS = Namespace('chat', description='Chat operations with Gemini AI')