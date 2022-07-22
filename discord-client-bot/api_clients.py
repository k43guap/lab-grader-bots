from config import get_settings
from lab_grader_client.api_client import ApiClient, AsyncApis

lab_grader_client = AsyncApis(ApiClient(get_settings().LAB_GRADER_HOST))
