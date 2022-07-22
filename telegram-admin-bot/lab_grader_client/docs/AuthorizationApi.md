# lab_grader_client.AuthorizationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**login**](AuthorizationApi.md#login) | **POST** /api/authorization/login | Login


# **login**
> StudentFromSheet login(non_authorized_student)

Login

### Example

```python
from __future__ import print_function
import time
import lab_grader_client
from lab_grader_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = lab_grader_client.AuthorizationApi()
non_authorized_student = lab_grader_client.NonAuthorizedStudent() # NonAuthorizedStudent | 

try:
    # Login
    api_response = api_instance.login(non_authorized_student)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuthorizationApi->login: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **non_authorized_student** | [**NonAuthorizedStudent**](NonAuthorizedStudent.md)|  | 

### Return type

[**StudentFromSheet**](StudentFromSheet.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Student successfully logged in |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

