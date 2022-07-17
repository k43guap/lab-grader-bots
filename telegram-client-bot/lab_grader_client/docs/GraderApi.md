# lab_grader_client.GraderApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_laboratory_works**](GraderApi.md#get_laboratory_works) | **GET** /api/grader/laboratory_works | Get Laboratory Works


# **get_laboratory_works**
> dict(str, LaboratoryWork) get_laboratory_works(course_name, authorized_student)

Get Laboratory Works

### Example

```python
from __future__ import print_function
import time
import lab_grader_client
from lab_grader_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = lab_grader_client.GraderApi()
course_name = 'course_name_example' # str | 
authorized_student = lab_grader_client.AuthorizedStudent() # AuthorizedStudent | 

try:
    # Get Laboratory Works
    api_response = api_instance.get_laboratory_works(course_name, authorized_student)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GraderApi->get_laboratory_works: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **course_name** | **str**|  | 
 **authorized_student** | [**AuthorizedStudent**](AuthorizedStudent.md)|  | 

### Return type

[**dict(str, LaboratoryWork)**](LaboratoryWork.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of labs for which repositories have been created |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

