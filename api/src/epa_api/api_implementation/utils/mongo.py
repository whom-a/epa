from typing import List, Tuple
from pymongo import MongoClient
from pymongo.database import Database
import os

class MongoUtils:
    """A class with helpful methods to interact with MongoDB"""
    def get_mongodb_env_variables() -> Tuple[str, int, str, str, List[str]]:
        """
        Get MongoDB env variables.
    
        :raises ValueError if one of the expected env variables are not set
        :return: A tupe containing the values of the env variables as such:
            - Hostname
            - Port
            - Username
            - Password
            - A list of collections
        :rtype: Tuple[str, int, str, str, List[str]]
        """
        
        output = []
        collection_output = []
        
        env_vars = [
            "EPA_MONGODB_HOSTNAME",
            "EPA_MONGODB_PORT",
            "EPA_MONGODB_USERNAME",
            "EPA_MONGODB_PASSWORD",
        ]
        
        env_collection_vars = [
            "EPA_MONGODB_USER_COLLECTION"
        ]
        
        for var in env_vars:
            val = os.getenv(var)
            if not val:
                raise ValueError(f"Expected environment variable {var} not set")
            output.append(val)
    
        for var in env_collection_vars:
            val = os.getenv(var)
            if not val:
                raise ValueError(f"Expected environment variable {var} not set") 
            collection_output.append(val)
            
        output.append(collection_output)
        return tuple(output)
        
    def get_mongodb_database_connection() -> Database:
        """
        Get MongoDB database connection.
    
        :raises ValueError if one of the expected env variables are not set.
        :return: A connection to a MongoDB database
        :rtype: pymongo.Database
        """
        
        hostname, port, username, password, _ = MongoUtils.get_mongodb_env_variables()
        uri = f"mongodb://{username}:{password}@{hostname}:{port}"
        
        client = MongoClient(uri)
        try:
            output = client["epa_database"]
            return output
        except:
            raise ValueError("Expected database epa_database does not exist")

    
    