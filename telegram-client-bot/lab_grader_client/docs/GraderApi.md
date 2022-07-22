# lab_grader_client.GraderApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_laboratory_works**](GraderApi.md#get_laboratory_works) | **GET** /api/grader/laboratory_works | Get Laboratory Works
[**rate**](GraderApi.md#rate) | **POST** /api/grader/rate | Rate


# **get_laboratory_works**
> dict(str, LaboratoryWork) get_laboratory_works(client_bot_id, course_name, authorized_student)

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
client_bot_id = 'client_bot_id_example' # str | 
course_name = 'course_name_example' # str | 
authorized_student = lab_grader_client.AuthorizedStudent() # AuthorizedStudent | 

try:
    # Get Laboratory Works
    api_response = api_instance.get_laboratory_works(client_bot_id, course_name, authorized_student)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GraderApi->get_laboratory_works: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **client_bot_id** | **str**|  | 
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

# **rate**
> RateResponse rate(client_bot_id, body_rate)

Rate

### Example

```python
from __future__ import print_function
import time
import lab_grader_client
from lab_grader_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = lab_grader_client.GraderApi()
client_bot_id = 'client_bot_id_example' # str | 
body_rate = lab_grader_client.BodyRate() # BodyRate | 

try:
    # Rate
    api_response = api_instance.rate(client_bot_id, body_rate)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GraderApi->rate: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **client_bot_id** | **str**|  | 
 **body_rate** | [**BodyRate**](BodyRate.md)|  | 

### Return type

[**RateResponse**](RateResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

