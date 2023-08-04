
import os

MONGO_URL = os.getenv('MONGO_URL', '')  
MONGO_DB = os.getenv('MONGO_DB', '') 
MONGO_PURCHASE_SUBS_COLL = 'treasury-purchase-subscriptions'
MONGO_CLIENTS_INFO_COLLECTION = os.getenv('MONGO_CLIENTS_INFO_COLLECTION', '')
MONGO_PLAN_COLLECTION = 'CatalogPremiums'
ENV = os.getenv('ENV', '') 
MOVEMENT_CONCEPT = os.getenv('MOVEMENT_CONCEPT', '')

GRPC_CLIENTS_INFO_HOST = os.getenv('GRPC_CLIENTS_INFO_HOST', '')
GRPC_CLIENTS_INFO_PORT = os.getenv('GRPC_CLIENTS_INFO_PORT', '')
GRPC_CB_MSG_ROUTER_HOST = os.getenv('GRPC_CB_MSG_ROUTER_HOST', '')
GRPC_CB_MSG_ROUTER_API_KEY = os.getenv('GRPC_CB_MSG_ROUTER_API_KEY', '')
GRPC_CB_MSG_ROUTER_PORT = os.getenv('GRPC_CB_MSG_ROUTER_PORT', '')
GRPC_LB_POLICY_NAME = os.getenv('GRPC_LB_POLICY_NAME', '')
GRPC_ENABLE_RETRIES = os.getenv('GRPC_ENABLE_RETRIES', '')
GRPC_KEEPALIVE_TIME_MS = os.getenv('GRPC_KEEPALIVE_TIME_MS', '')

DB_SQL_USER = os.getenv('DB_SQL_USER', '')
DB_SQL_PASSWORD = os.getenv('DB_SQL_PASSWORD', '')
DB_SQL_HOST = os.getenv('DB_SQL_HOST', '')
DB_SQL_PORT = os.getenv('DB_SQL_PORT', '')
DB_SQL_DATABASE = os.getenv('DB_SQL_DATABASE', '')
DB_SQL_SCHEMA = os.getenv('DB_SQL_SCHEMA', '')

if ENV == 'local':
    MONGO_URL = f"mongodb://user:pwd@localhost:27017/?tls=false"
