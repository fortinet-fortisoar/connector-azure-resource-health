from .operations import check_health_ex, operations
from connectors.core.connector import Connector, get_logger, ConnectorError

logger = get_logger("azure-resource-health")


class MSManagmentActivity(Connector):
    def execute(self, config, operation, params, **kwargs):
        try:
            connector_info = {"connector_name": self._info_json.get('name'),
                              "connector_version": self._info_json.get('version')}
            operation = operations.get(operation)
        except Exception as err:
            logger.exception(err)
            raise ConnectorError(err)
        return operation(config, params, connector_info)

    def check_health(self, config):
        logger.info('starting health check')
        connector_info = {"connector_name": self._info_json.get('name'),
                          "connector_version": self._info_json.get('version')}
        check_health_ex(config, connector_info)
        logger.info('completed health check no errors')