/*
 * Copyright 2022 Engineering Ingegneria Informatica S.p.A.
 *
 * This file is part of iotagent-opcua
 *
 * iotagent-opcua is free software: you can redistribute it and/or
 * modify it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the License,
 * or (at your option) any later version.
 *
 * iotagent-opcua is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public
 * License along with iotagent-opcua.
 * If not, see http://www.gnu.org/licenses/.
 *
 * For those usages not covered by the GNU Affero General Public License
 * please contact with::[manfredi.pistone@eng.it, gabriele.deluca@eng.it, walterdomenico.vergara@eng.it, mattiagiuseppe.marzano@eng.it]
 */

const config = {};

config.iota = {
    /**
     * Configures the log level. Appropriate values are: FATAL, ERROR, INFO, WARN and DEBUG.
     */
    logLevel: process.env.LOGLEVEL,
    /**
     * When this flag is active, the IoTAgent will add the TimeInstant attribute to every entity created, as well
     * as a TimeInstant metadata to each attribute, with the current timestamp.
     */
    timestamp: false,
    /**
     * Context Broker configuration. Defines the connection information to the instance of the Context Broker where
     * the IoT Agent will send the device data.
     */
    contextBroker: {
        /**
         * Host where the Context Broker is located.
		 * ******************** Overriden in the docker file by IOTA_CB_HOST
         */
        host: 'localhost',
        /**
         * Port where the Context Broker is listening.
		 * ******************** Overriden in the docker file by IOTA_CB_PORT
         */
        port: '1026',
        /**
         * Version of the Context Broker (v2 or ld)
         */
        ngsiVersion: 'v2',
        /**
         * JSON LD Context
         */
        jsonLdContext: 'https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld',
        /**
         * Used as fallbackTenant
		 * * ******************** Overriden in the docker file by IOTA_FALLBACK_TENANT
         */
        service: 'opcua_car',
        /**
         * Used as fallbackPath
		 * * ******************** Overriden in the docker file by IOTA_FALLBACK_PATH
         */
        subservice: '/demo'
    },
    /**
     * Configuration of the North Port of the IoT Agent.
     */
    server: {
        /**
         * Port where the IoT Agent will be listening for NGSI and Provisioning requests.
		 * ******************** Overriden in the docker file by IOTA_NORTH_PORT
         */
        port: 4041
    },

    /**
     * Configuration for secured access to instances of the Context Broker secured with a PEP Proxy.
     * For the authentication mechanism to work, the authentication attribute in the configuration has to be fully
     * configured, and the authentication.enabled subattribute should have the value `true`.
     *
     * The Username and password should be considered as sensitive data and should not be stored in plaintext.
     * Either encrypt the config and decrypt when initializing the instance or use environment variables secured by
     * docker secrets.
     */
    //authentication: {
    //enabled: false,
    /**
     * Type of the Identity Manager which is used when authenticating the IoT Agent.
     */
    //type: 'keystone',
    /**
     * Name of the additional header passed to hold the identity of the IoT Agent
     */
    //header: 'X-Auth-Token',
    /**
     * Hostname of the Identity Manager.
     */
    //host: 'localhost',
    /**
     * Port of the Identity Manager.
     */
    //port: '5000',
    /**
     * Username for the IoT Agent - Note this should not be stored in plaintext.
     */
    //user: 'IOTA_AUTH_USER',
    /**
     * Password for the IoT Agent - Note this should not be stored in plaintext.
     */
    //password: 'IOTA_AUTH_PASSWORD',
    /**
     * OAuth2 client ID - Note this should not be stored in plaintext.
     */
    //clientId: 'IOTA_AUTH_CLIENT_ID',
    /**
     * OAuth2 client secret - Note this should not be stored in plaintext.
     */
    //clientSecret: 'IOTA_AUTH_CLIENT_SECRET'
    //},

    /**
     * Defines the configuration for the Device Registry, where all the information about devices and configuration
     * groups will be stored. There are currently just two types of registries allowed:
     *
     * - 'memory': transient memory-based repository for testing purposes. All the information in the repository is
     *             wiped out when the process is restarted.
     *
     * - 'mongodb': persistent MongoDB storage repository. All the details for the MongoDB configuration will be read
     *             from the 'mongodb' configuration property.
	 * ******************** Overriden in the docker file by IOTA_REGISTRY_TYPE
     */
    deviceRegistry: {
        type: 'mongodb'
    },
    /**
     * Mongo DB configuration section. This section will only be used if the deviceRegistry property has the type
     * 'mongodb'.
     */
    mongodb: {
        /**
         * Host where MongoDB is located. If the MongoDB used is a replicaSet, this property will contain a
         * comma-separated list of the instance names or IPs.
		 * ******************** Overriden in the docker file by IOTA_MONGO_HOST
         */
        host: 'localhost',
        /**
         * Port where MongoDB is listening. In the case of a replicaSet, all the instances are supposed to be listening
         * in the same port.
		 * ******************** Overriden in the docker file by IOTA_MONGO_PORT
         */
        port: '27017',
        /**
         * Name of the Mongo database that will be created to store IoT Agent data.
		 * ******************** Overriden in the docker file by IOTA_MONGO
         */
        db: 'iotagent_opcua'
    },
    /**
     * Types array for static configuration of services. Check documentation in the IoT Agent Library for Node.js for
     *  further details:
     *
     *      https://github.com/Engineering-Research-and-Development/iotagent-opcua#type-configuration
	 * 
	 * 	Values overriden by process.env.VARIABLE_NAME from docker-compose file who inherits with "VARIABLE_NAME=${VARIABLE_NAME}" from .env file
	 * 	PLC: {...} is the only value I can't override
	 * 
     */
    types: {
		PLC: {
			active: [
				{
					name: process.env.OCB_ID_PROCESS,
					type: 'Text'
				}
                // {
				// 	name: process.env.OCB_ID_MACHINE,
				// 	type: 'Boolean'
				// }
			],
			lazy: [],
			commands: []
		}
	},
	contexts: [
		{
			id: process.env.DEVICE_ID,
			type: process.env.DEVICE_TYPE,
			mappings: [
				{
					ocb_id: process.env.OCB_ID_PROCESS,
					opcua_id: process.env.OPCUA_ID_PROCESS,
					inputArguments: []
				}
                // {
				// 	ocb_id: process.env.OCB_ID_MACHINE,
				// 	opcua_id: process.env.OPCUA_ID_MACHINE,
				// 	inputArguments: []
				// }
			]
		}
	],
	contextSubscriptions: [],
    /**
     * Default service, for IoT Agent installations that won't require preregistration.
	 * 
	 * 	Values overriden by process.env.VARIABLE_NAME from docker-compose file who inherits with "VARIABLE_NAME=${VARIABLE_NAME}" from .env file
	 * 
     */
    service: process.env.FIWARE_SERVICE,
    /**
     * Default subservice, for IoT Agent installations that won't require preregistration.
	 * 
	 * 	Values overriden by process.env.VARIABLE_NAME from docker-compose file who inherits with "VARIABLE_NAME=${VARIABLE_NAME}" from .env file
	 * 
     */
    subservice: process.env.FIWARE_SERVICEPATH,
    /**
     * URL Where the IoT Agent Will listen for incoming updateContext and queryContext requests (for commands and
     * passive attributes). This URL will be sent in the Context Registration requests.
	 * ******************** Overriden in the docker file by IOTA_PROVIDER_URL
     */
    providerUrl: 'http://localhost:4041',
    /**
     * Default maximum expire date for device registrations.
     */
    deviceRegistrationDuration: 'P20Y',
    /**
     * Default type, for IoT Agent installations that won't require preregistration.
     */
    defaultType: 'PLC',
    /**
     * Default resource of the IoT Agent. This value must be different for every IoT Agent connecting to the IoT
     * Manager.
     */
    defaultResource: '/iot/opcua',
    /**
     * flag indicating whether the incoming measures to the IoTAgent should be processed as per the "attributes" field.
     */
    explicitAttrs: false
};

config.opcua = {
    /**
     * Subscription options for OPC UA connection.
     */
    subscription: {
        maxNotificationsPerPublish: 1000,
        publishingEnabled: true,
        requestedLifetimeCount: 100,
        requestedMaxKeepAliveCount: 10,
        requestedPublishingInterval: 1000,
        priority: 128
    },
    /**
     * Endpoint where the IoT Agent will listen for an active OPC UA Server.
	 * ******************** Overriden in the docker file by IOTA_OPCUA_ENDPOINT
     */
    endpoint: 'opc.tcp://localhost:5001/UA/CarServer',
    /**
     * Security Mode to access OPC UA Server.
	 * ******************** Overriden in the docker file by IOTA_OPCUA_SECURITY_MODE
     */
    securityMode: 'None',
    /**
     * Security Policy to access OPC UA Server.
	 * ******************** Overriden in the docker file by IOTA_OPCUA_SECURITY_POLICY
     */
    securityPolicy: 'None',
    /**
     * Username to access OPC UA Server.
	 * ******************** Overriden in the docker file by IOTA_OPCUA_SECURITY_USERNAME
     */
    username: null,
    /**
     * Password to access OPC UA Server.
	 * ******************** Overriden in the docker file by IOTA_OPCUA_SECURITY_PASSWORD
     */
    password: null,
    /**
     * Flag indicating whether the OPC UA variables readings should be handled as single subscription.
	 * ******************** Overriden in the docker file by IOTA_OPCUA_UNIQUE_SUBSCRIPTION
     */
    uniqueSubscription: false
};

config.mappingTool = {
    /**
     *  Boolean property to assess whether enable polling in MappingTool or not
	 * ******************** Overriden in the docker file by IOTA_OPCUA_MT_POLLING
     */
    polling: false,
    /**
     * agentId prefix to be assigned to the newly generated entity from MappingTool execution
	 * ******************** Overriden in the docker file by IOTA_OPCUA_MT_AGENT_ID
     */
    agentId: 'age01_',
    /**
     * Namespaces to ignore when crawling nodes from OPC UA Server
	 * ******************** Overriden in the docker file by IOTA_OPCUA_MT_NAMESPACE_IGNORE
     */
    namespaceIgnore: '0,1,2,3',
    /**
     * entityId to be assigned to the newly generated entity from MappingTool execution
	 * ******************** Overriden in the docker file by IOTA_OPCUA_MT_ENTITY_ID
     */
    entityId: 'age01_Car',
    /**
     * entityType to be assigned to the newly generated entity from MappingTool execution
	 * ******************** Overriden in the docker file by IOTA_OPCUA_MT_ENTITY_TYPE
     */
    entityType: 'Device'
};

/**
 * map {name: function} of extra transformations avaliable at JEXL plugin
 *  see https://github.com/telefonicaid/iotagent-node-lib/tree/master/doc/expressionLanguage.md#available-functions
 */

config.jexlTransformations = {};

/**
 * flag indicating whether the incoming notifications to the IoTAgent should be processed using the bidirectionality
 * plugin from the latest versions of the library or the OPCUA-specific configuration retrieval mechanism.
 */
config.configRetrieval = false;
/**
 * Default API Key, to use with device that have been provisioned without a Configuration Group.
 */
config.defaultKey = 'iot';
/**
 * Default transport protocol when no transport is provisioned through the Device Provisioning API.
 */
config.defaultTransport = 'OPCUA';
/**
 * flag indicating whether the node server will be executed in multi-core option (true) or it will be a
 * single-thread one (false).
 */
//config.multiCore = false;
/**
 * flag indicating whether or not to provision the Group and Device automatically
 */
config.autoprovision = true;

module.exports = config;
