from requests import request, exceptions as req_exceptions
from .microsoft_api_auth import *
from connectors.core.connector import get_logger, ConnectorError
from .constants import *

logger = get_logger("azure-resource-health")


def check_health_ex(config, connector_info):
    try:
        ms = MicrosoftAuth(config)
        return ms.check(config, connector_info)
    except Exception as err:
        raise ConnectorError(str(err))


def api_request(method, endpoint, connector_info, config, params={}, data={}, headers={}):
    try:
        ms = MicrosoftAuth(config)
        endpoint = ms.host + endpoint

        token = ms.validate_token(config, connector_info)
        headers["Authorization"] = token
        headers["Content-Type"] = "application/json"

        try:
            logger.error(f"\n-------------- method: {method} || endpoint: {endpoint} || headers: {headers} || params: {params} || data: {data} || verify: {ms.verify_ssl} ---------------\n")
            response = request(method, endpoint, headers=headers, params=params,
                               data=data, verify=ms.verify_ssl)

            if response.status_code in [200, 201, 204]:
                if response.text != "":
                    return response.json()
                else:
                    return True
            else:
                if response.text != "":
                    err_resp = response.json()
                    failure_msg = err_resp['error']['message']
                    error_msg = 'Response [{0}:{1} Details: {2}]'.format(response.status_code, response.reason,
                                                                         failure_msg if failure_msg else '')
                else:
                    error_msg = 'Response [{0}:{1}]'.format(response.status_code, response.reason)
                logger.error(error_msg)
                raise ConnectorError(error_msg)
        except req_exceptions.SSLError:
            logger.error('An SSL error occurred')
            raise ConnectorError('An SSL error occurred')
        except req_exceptions.ConnectionError:
            logger.error('A connection error occurred')
            raise ConnectorError('A connection error occurred')
        except req_exceptions.Timeout:
            logger.error('The request timed out')
            raise ConnectorError('The request timed out')
        except req_exceptions.RequestException:
            logger.error('There was an error while handling the request')
            raise ConnectorError('There was an error while handling the request')
        except Exception as err:
            raise ConnectorError(str(err))
    except Exception as err:
        raise ConnectorError(str(err))


def get_url_and_params(function_name, config, params, connector_info):
    subscription_id = params.get("subscription_id", "")
    resource_group_name = params.get("resource_group_name", "")
    resource_provider_name = params.get("resource_provider_name", "")
    resource_type = params.get("resource_type", "")
    resource_name = params.get("resource_name", "")
    filter_query = params.get("filter")
    query_params = {
        "api-version": API_VERSION
    }
    if filter_query:
        query_params["$filter"] = filter_query
    endpoint = ""
    if function_name == FuncName.GET_AVAILABILITY_STATUS:
        endpoint = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/{resource_provider_name}/{resource_type}/{resource_name}/providers/Microsoft.ResourceHealth/availabilityStatuses/current"
    elif function_name == FuncName.GET_AVAILABILITY_STATUS_LIST:
        endpoint = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/{resource_provider_name}/{resource_type}/{resource_name}/providers/Microsoft.ResourceHealth/availabilityStatuses"
    elif function_name == FuncName.GET_AVAILABILITY_STATUS_BY_RESOURCE_GROUP:
        endpoint = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.ResourceHealth/availabilityStatuses"
    elif function_name == FuncName.GET_AVAILABILITY_STATUS_BY_SUBSCRIPTION_ID:
        endpoint = f"/subscriptions/{subscription_id}/providers/Microsoft.ResourceHealth/availabilityStatuses"
    elif function_name == FuncName.GET_EVENT_LIST_FOR_RESOURCE:
        endpoint = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/{resource_provider_name}/{resource_type}/{resource_name}/providers/Microsoft.ResourceHealth/events"
    elif function_name == FuncName.GET_EVENT_LIST_FOR_SUBSCRIPTION_ID:
        endpoint = f"/subscriptions/{subscription_id}/providers/Microsoft.ResourceHealth/events"
    elif function_name == FuncName.GET_EVENT_LIST_FOR_TENANT_ID:
        endpoint = "/providers/Microsoft.ResourceHealth/events"
    return endpoint, query_params


def get_availability_status(config, params, connector_info):
    try:
        endpoint, query_params = get_url_and_params(FuncName.GET_AVAILABILITY_STATUS, config, params, connector_info)
        response = api_request("GET", endpoint, connector_info, config, query_params)
        return response
    except Exception as err:
        raise ConnectorError(str(err))


def get_availability_status_list(config, params, connector_info):
    try:
        endpoint, query_params = get_url_and_params(FuncName.GET_AVAILABILITY_STATUS_LIST, config, params, connector_info)
        response = api_request("GET", endpoint, connector_info, config, query_params)
        return response
    except Exception as err:
        raise ConnectorError(str(err))


def get_availability_status_by_resource_group(config, params, connector_info):
    try:
        endpoint, query_params = get_url_and_params(FuncName.GET_AVAILABILITY_STATUS_BY_RESOURCE_GROUP, config, params, connector_info)
        response = api_request("GET", endpoint, connector_info, config, query_params)
        return response
    except Exception as err:
        raise ConnectorError(str(err))


def get_availability_status_by_subscription_id(config, params, connector_info):
    try:
        endpoint, query_params = get_url_and_params(FuncName.GET_AVAILABILITY_STATUS_BY_SUBSCRIPTION_ID, config, params, connector_info)
        response = api_request("GET", endpoint, connector_info, config, query_params)
        return response
    except Exception as err:
        raise ConnectorError(str(err))


def get_event_list_for_resource(config, params, connector_info):
    try:
        endpoint, query_params = get_url_and_params(FuncName.GET_EVENT_LIST_FOR_RESOURCE, config, params, connector_info)
        response = api_request("GET", endpoint, connector_info, config, query_params)
        return response
    except Exception as err:
        raise ConnectorError(str(err))


def get_event_list_for_subscription_id(config, params, connector_info):
    try:
        endpoint, query_params = get_url_and_params(FuncName.GET_EVENT_LIST_FOR_SUBSCRIPTION_ID, config, params, connector_info)
        response = api_request("GET", endpoint, connector_info, config, query_params)
        return response
    except Exception as err:
        raise ConnectorError(str(err))


def get_event_list_for_tenant_id(config, params, connector_info):
    try:
        endpoint, query_params = get_url_and_params(FuncName.GET_EVENT_LIST_FOR_TENANT_ID, config, params, connector_info)
        response = api_request("GET", endpoint, connector_info, config, query_params)
        return response
    except Exception as err:
        raise ConnectorError(str(err))


operations = {
    FuncName.GET_AVAILABILITY_STATUS: get_availability_status,
    FuncName.GET_AVAILABILITY_STATUS_LIST: get_availability_status_list,
    FuncName.GET_AVAILABILITY_STATUS_BY_RESOURCE_GROUP: get_availability_status_by_resource_group,
    FuncName.GET_AVAILABILITY_STATUS_BY_SUBSCRIPTION_ID: get_availability_status_by_subscription_id,
    FuncName.GET_EVENT_LIST_FOR_RESOURCE: get_event_list_for_resource,
    FuncName.GET_EVENT_LIST_FOR_SUBSCRIPTION_ID: get_event_list_for_subscription_id,
    FuncName.GET_EVENT_LIST_FOR_TENANT_ID: get_event_list_for_tenant_id
}
