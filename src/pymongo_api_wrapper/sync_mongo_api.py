from typing import Union
from warnings import deprecated

import bson
import pymongo


@deprecated
def string_to_object_id(id_string: str):
    """
    Convert a string to a mongo object id

    :param id_string: string to convert

    :return: mongo object id
    """
    return bson.ObjectId(id_string)


@deprecated
def object_id_to_string(id_object: bson.ObjectId):
    """
    Convert a mongo object id to a string

    :param id_object: mongo object id to convert

    :return: string
    """
    return str(id_object)


class MongoAPI:
    client: pymongo.MongoClient
    db_name: str

    def close(self):
        """
        Close the connection to MongoDB

        :return:
        """
        self.client.close()

    def __init__(self, db_address: str,
                 db_name: str,
                 db_username: str,
                 db_password: str,
                 service: str = "mongodb",
                 **kwargs):
        """
        :param db_address: Database Address like db.something.mongodb.net
        :param db_name: name of the database
        :param db_username: username
        :param db_password: password to username

        :param kwargs: Passed to the MongoClient.__init__ method. (i.e. tlsCAFile=certifi.where())
        """
        if service not in ("mongodb+srv", "mongodb"):
            raise ValueError("service must be either 'mongodb+srv' or 'mongodb'")

        # initialising connection to Mongo
        self.client = pymongo.MongoClient(f"{service}://{db_username}:{db_password}@{db_address}/"
                                          f"{db_name}?retryWrites=true&w=majority", **kwargs)

        self.db_name = db_name

    def collection(self, collection: str):
        return self.client[self.db_name][collection]

    def find_one(self, collection: str, filter_dict: dict = None, projection_dict: dict = None, sort: list = None):
        """
        Query the database.

        :param collection: Collection name string
        :param filter_dict: A dict specifying elements which must be present for a document to be included in the res
        :param projection_dict: A dict of field names that should be returned in the result
        :param sort: A list of (key, direction) pairs specifying the sort order for this query

        :return:
        """

        col = self.client[self.db_name][collection]

        return col.find_one(filter=filter_dict, projection=projection_dict, sort=sort)

    def find(self, collection: str, filter_dict: dict = None, projection_dict: dict = None, sort: list = None,
             skip:int = 0, limit: int = 0):
        """
        Query the database.

        :param collection: Collection name string
        :param filter_dict: A dict specifying elements which must be present for a document to be included in the result
        :param projection_dict: A dict of field names that should be returned in the result
        :param sort: A list of (key, direction) pairs specifying the sort order for this query
        :param skip: Number of documents in order to skip
        :param limit: Number of documents to return

        :return:
        """

        col = self.client[self.db_name][collection]

        return list(col.find(filter=filter_dict, projection=projection_dict, sort=sort, skip=skip, limit=limit))

    def insert_one(self, collection: str, document_dict: dict = None):
        """
        Insert a single document.

        :param collection: Collection name string
        :param document_dict:  The document to insert

        :return: inserted id
        """
        if document_dict is None:
            document_dict = {}

        col = self.client[self.db_name][collection]

        result = col.insert_one(document=document_dict)

        return result.inserted_id

    def insert(self, collection: str, document_list: list = None):
        """
        Insert an iterable of documents.

        :param collection: Collection name string
        :param document_list:  The documents to insert into the db. Needs to be a list containing documents

        :return: inserted id
        """
        if document_list is None or len(document_list) < 1:
            return

        col = self.client[self.db_name][collection]

        result = col.insert_many(documents=document_list)

        return result.inserted_ids

    def update_one(self, collection: str, filter_dict: dict = None, update_dict: dict | list = None, upsert: bool = False):
        """
        Update a single document matching the filter.

        :param collection: Collection name string
        :param filter_dict: A dict specifying elements which must be present for a document to be included in the result
        :param update_dict: A dict with the modifications to apply
        :param upsert: If True, perform an insert if no documents match the filter

        :return: modified count
        """

        col = self.client[self.db_name][collection]

        result = col.update_one(filter=filter_dict, update=update_dict, upsert=upsert)

        return result.modified_count

    def update(self, collection: str, filter_dict: dict = None, update_dict: Union[list, dict] = None, upsert: bool = False):
        """
        Update one or more documents that match the filter.

        :param collection: Collection name string
        :param filter_dict: A dict specifying elements which must be present for a document to be included in the result
        :param update_dict: A dict with the modifications to apply
        :param upsert: If True, perform an insert if no documents match the filter

        :return: modified count
        """

        col = self.client[self.db_name][collection]

        result = col.update_many(filter=filter_dict, update=update_dict, upsert=upsert)

        return result.modified_count

    def delete_one(self, collection: str, filter_dict: dict = None):
        """
        Delete a single document matching the filter.

        :param collection: Collection name string
        :param filter_dict A dict specifying elements which must be present for a document to be included in the result

        :return: deleted count
        """

        col = self.client[self.db_name][collection]

        result = col.delete_one(filter=filter_dict)

        return result.deleted_count

    def delete(self, collection: str, filter_dict: dict = None):
        """
        Delete one or more documents matching the filter.

        :param collection: Collection name string
        :param filter_dict: A dict specifying elements which must be present for a document to be included in the result

        :return: deleted count
        """

        col = self.client[self.db_name][collection]

        result = col.delete_many(filter=filter_dict)

        return result.deleted_count

    def count(self, collection: str, filter_dict: dict = None):
        """
        Count the number of documents in this collection.

        :param collection: Collection name string
        :param filter_dict: A dict specifying elements which must be present for a document to be included in the result

        :return:
        """
        if filter_dict is None:
            filter_dict = {}

        col = self.client[self.db_name][collection]
        return col.count_documents(filter=filter_dict)

    def aggregate(self, collection: str, pipeline: list = None):
        """
        Perform an aggregation using the aggregation framework on this collection.

        :param collection: Collection name string
        :param pipeline: A list of aggregation pipeline stages

        :return:
        """
        if pipeline is None:
            pipeline = []

        col = self.client[self.db_name][collection]
        return list(col.aggregate(pipeline=pipeline))

    def find_one_and_update(self,
                            collection: str,
                            update_dict: Union[list, dict],
                            filter_dict: Union[dict, list] = None,
                            projection_dict: dict = None,
                            sort: list = None,
                            return_document: pymongo.ReturnDocument = pymongo.ReturnDocument.AFTER) -> dict | None:
        """
        Find a document and update it in one atomic operation.

        :param collection: Collection name string
        :param update_dict: A dict with the modifications to apply
        :param filter_dict: A dict specifying elements which must be present for a document to be included in the result
        :param projection_dict: A dict of field names that should be returned in the result
        :param sort: A list of (key, direction) pairs specifying the sort order for this query
        :param return_document: state in which the document is to be returned.

        :return:
        """
        if filter_dict is None:
            filter_dict = {}

        col = self.client[self.db_name][collection]

        result = col.find_one_and_update(filter=filter_dict,
                                         update=update_dict,
                                         projection=projection_dict,
                                         sort=sort,
                                         # INFO, that's correct pymongo.ReturnDocument is a wrapper for bool.
                                         return_document=return_document)

        return result
