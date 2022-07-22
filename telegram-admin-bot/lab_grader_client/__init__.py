import inspect

from pydantic import BaseModel

from lab_grader_client import models
from lab_grader_client.api_client import ApiClient, AsyncApis, SyncApis  # noqa F401

for model in inspect.getmembers(models, inspect.isclass):
    if model[1].__module__ == "lab_grader_client.models":
        model_class = model[1]
        if isinstance(model_class, BaseModel):
            model_class.update_forward_refs()
