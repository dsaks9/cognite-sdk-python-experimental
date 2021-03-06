import threading
from typing import Any, Dict, List

from cognite.client.data_classes import Asset as NonExperimentalAsset
from cognite.client.data_classes._base import *
from cognite.client.data_classes.shared import TimestampRange


# GenPropertyClass: AggregateResultItem
class AggregateResultItem(dict):
    """Aggregated metrics of the asset

    Args:
        child_count (int): Number of direct descendants for the asset
        depth (int): Asset path depth (number of levels below root node).
        path (List[Dict[str, Any]]): IDs of assets on the path to the asset.
    """

    def __init__(self, child_count: int = None, depth: int = None, path: List[Dict[str, Any]] = None, **kwargs):
        self.child_count = child_count
        self.depth = depth
        self.path = path
        self.update(kwargs)

    child_count = CognitePropertyClassUtil.declare_property("childCount")
    depth = CognitePropertyClassUtil.declare_property("depth")
    path = CognitePropertyClassUtil.declare_property("path")

    # GenStop


# GenClass: Asset, ExternalAsset
class Asset(NonExperimentalAsset):
    """No description.

    Args:
        id (int): A server-generated ID for the object.
        external_id (str): External Id provided by client. Should be unique within the project.
        name (str): Name of asset. Often referred to as tag.
        parent_id (int): A server-generated ID for the object.
        parent_external_id (str): The external ID of the parent. The property is omitted if the asset doesn't have a parent or if the parent doesn't have externalId.
        description (str): Description of asset.
        data_set_id (int): A server-generated ID for the object.
        metadata (Dict[str, str]): Custom, application specific metadata. String key -> String value. Limits: Key are at most 128 bytes. Values are at most 10240 bytes. Up to 256 key-value pairs. Total size is at most 10240.
        source (str): The source of this asset
        types (List[Dict[str, Any]]): No description.
        labels (List[Dict[str, Any]]): A list of the labels associated with this asset.
        created_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        last_updated_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        root_id (int): A server-generated ID for the object.
        aggregates (Union[Dict[str, Any], AggregateResultItem]): Aggregated metrics of the asset
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self,
        id: int = None,
        external_id: str = None,
        name: str = None,
        parent_id: int = None,
        parent_external_id: str = None,
        description: str = None,
        data_set_id: int = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        types: List[Dict[str, Any]] = None,
        labels: List[Dict[str, Any]] = None,
        created_time: int = None,
        last_updated_time: int = None,
        root_id: int = None,
        aggregates: Union[Dict[str, Any], AggregateResultItem] = None,
        cognite_client=None,
    ):
        self.id = id
        self.external_id = external_id
        self.name = name
        self.parent_id = parent_id
        self.parent_external_id = parent_external_id
        self.description = description
        self.data_set_id = data_set_id
        self.metadata = metadata
        self.source = source
        self.types = types
        self.labels = labels
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.root_id = root_id
        self.aggregates = aggregates
        self._cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: Union[Dict, str], cognite_client=None):
        instance = super(Asset, cls)._load(resource, cognite_client)
        if isinstance(resource, Dict):
            if instance.aggregates is not None:
                instance.aggregates = AggregateResultItem(**instance.aggregates)
        return instance

    # GenStop

    def __hash__(self):
        return hash(self.external_id)

    def parent(self) -> "Asset":
        """Returns this assets parent.

        Returns:
            Asset: The parent asset.
        """
        if self.parent_id is None:
            raise ValueError("parent_id is None")
        return self._cognite_client.assets.retrieve(id=self.parent_id)

    def children(self) -> "AssetList":
        """Returns the children of this asset.

        Returns:
            AssetList: The requested assets
        """
        return self._cognite_client.assets.list(parent_ids=[self.id], limit=None)

    def subtree(self, depth: int = None) -> "AssetList":
        """Returns the subtree of this asset up to a specified depth.

        Args:
            depth (int, optional): Retrieve assets up to this depth below the asset.

        Returns:
            AssetList: The requested assets sorted topologically.
        """
        return self._cognite_client.assets.retrieve_subtree(id=self.id, depth=depth)

    def time_series(self, **kwargs) -> "TimeSeriesList":
        """Retrieve all time series related to this asset.

        Returns:
            TimeSeriesList: All time series related to this asset.
        """
        return self._cognite_client.time_series.list(asset_ids=[self.id], **kwargs)

    def sequences(self, **kwargs) -> "SequenceList":
        """Retrieve all sequences related to this asset.

        Returns:
            SequenceList: All sequences related to this asset.
        """
        return self._cognite_client.sequences.list(asset_ids=[self.id], **kwargs)

    def events(self, **kwargs) -> "EventList":
        """Retrieve all events related to this asset.

        Returns:
            EventList: All events related to this asset.
        """

        return self._cognite_client.events.list(asset_ids=[self.id], **kwargs)

    def files(self, **kwargs) -> "FileMetadataList":
        """Retrieve all files metadata related to this asset.

        Returns:
            FileMetadataList: Metadata about all files related to this asset.
        """
        return self._cognite_client.files.list(asset_ids=[self.id], **kwargs)

    def to_pandas(
        self, expand: List[str] = ("metadata", "aggregates"), ignore: List[str] = None, camel_case: bool = True
    ):
        """Convert the instance into a pandas DataFrame.

        Args:
            expand (List[str]): List of row keys to expand, only works if the value is a Dict.
            ignore (List[str]): List of row keys to not include when converting to a data frame.
            camel_case (bool): Convert column names to camel case (e.g. `externalId` instead of `external_id`)

        Returns:
            pandas.DataFrame: The dataframe.
        """
        return super().to_pandas(expand=expand, ignore=ignore, camel_case=camel_case)


# GenUpdateClass: AssetChange
class AssetUpdate(CogniteUpdate):
    """Changes applied to asset

    Args:
        id (int): A server-generated ID for the object.
        external_id (str): External Id provided by client. Should be unique within the project.
    """

    class _PrimitiveAssetUpdate(CognitePrimitiveUpdate):
        def set(self, value: Any) -> "AssetUpdate":
            return self._set(value)

    class _ObjectAssetUpdate(CogniteObjectUpdate):
        def set(self, value: Dict) -> "AssetUpdate":
            return self._set(value)

        def add(self, value: Dict) -> "AssetUpdate":
            return self._add(value)

        def remove(self, value: List) -> "AssetUpdate":
            return self._remove(value)

    class _ListAssetUpdate(CogniteListUpdate):
        def set(self, value: List) -> "AssetUpdate":
            return self._set(value)

        def add(self, value: List) -> "AssetUpdate":
            return self._add(value)

        def remove(self, value: List) -> "AssetUpdate":
            return self._remove(value)

    @property
    def external_id(self):
        return AssetUpdate._PrimitiveAssetUpdate(self, "externalId")

    @property
    def name(self):
        return AssetUpdate._PrimitiveAssetUpdate(self, "name")

    @property
    def description(self):
        return AssetUpdate._PrimitiveAssetUpdate(self, "description")

    @property
    def data_set_id(self):
        return AssetUpdate._PrimitiveAssetUpdate(self, "dataSetId")

    @property
    def metadata(self):
        return AssetUpdate._ObjectAssetUpdate(self, "metadata")

    @property
    def source(self):
        return AssetUpdate._PrimitiveAssetUpdate(self, "source")

    @property
    def parent_id(self):
        return AssetUpdate._PrimitiveAssetUpdate(self, "parentId")

    @property
    def parent_external_id(self):
        return AssetUpdate._PrimitiveAssetUpdate(self, "parentExternalId")

    # GenStop

    @property
    def types(self):
        raise Exception("Use the put_type and remove_type functions to handle type updates")

    def put_type(self, properties: Dict[str, Any], version: int, id: int = None, external_id: str = None):
        """Upsert the type information on the asset"""
        if self._update_object.get("types") is None:
            self._update_object["types"] = {}
        if self._update_object["types"].get("put") is None:
            self._update_object["types"]["put"] = []
        self._update_object["types"]["put"].append(
            {"type": {"id": id, "externalId": external_id, "version": version}, "properties": properties}
        )
        return self

    def remove_type(self, version: int, id: int = None, external_id: str = None):
        """Remove type information from an asset"""
        if self._update_object.get("types") is None:
            self._update_object["types"] = {}
        if self._update_object["types"].get("remove") is None:
            self._update_object["types"]["remove"] = []
        self._update_object["types"]["remove"].append({"id": id, "externalId": external_id, "version": version})
        return self

    @property
    def labels(self):
        raise Exception("Use the put_label and remove_label functions to handle label updates")

    def put_label(self, external_id: str = None):
        """Upsert the label on the asset"""
        if self._update_object.get("labels") is None:
            self._update_object["labels"] = {}
        if self._update_object["labels"].get("put") is None:
            self._update_object["labels"]["put"] = []
        self._update_object["labels"]["put"].append({"externalId": external_id})
        return self

    def remove_label(self, external_id: str = None):
        """Remove the label from an asset"""
        if self._update_object.get("labels") is None:
            self._update_object["labels"] = {}
        if self._update_object["labels"].get("remove") is None:
            self._update_object["labels"]["remove"] = []
        self._update_object["labels"]["remove"].append({"externalId": external_id})
        return self


class AssetList(CogniteResourceList):
    _RESOURCE = Asset
    _UPDATE = AssetUpdate

    def __init__(self, resources: List[Any], cognite_client=None):
        super().__init__(resources, cognite_client)
        self._retrieve_chunk_size = 100

    def time_series(self) -> "TimeSeriesList":
        """Retrieve all time series related to these assets.

        Returns:
            TimeSeriesList: All time series related to the assets in this AssetList.
        """
        from cognite.client.data_classes import TimeSeriesList

        return self._retrieve_related_resources(TimeSeriesList, self._cognite_client.time_series)

    def sequences(self) -> "SequenceList":
        """Retrieve all sequences related to these assets.

        Returns:
            SequenceList: All sequences related to the assets in this AssetList.
        """
        from cognite.client.data_classes import SequenceList

        return self._retrieve_related_resources(SequenceList, self._cognite_client.sequences)

    def events(self) -> "EventList":
        """Retrieve all events related to these assets.

        Returns:
            EventList: All events related to the assets in this AssetList.
        """
        from cognite.client.data_classes import EventList

        return self._retrieve_related_resources(EventList, self._cognite_client.events)

    def files(self) -> "FileMetadataList":
        """Retrieve all files metadata related to these assets.

        Returns:
            FileMetadataList: Metadata about all files related to the assets in this AssetList.
        """
        from cognite.client.data_classes import FileMetadataList

        return self._retrieve_related_resources(FileMetadataList, self._cognite_client.files)

    def _retrieve_related_resources(self, resource_list_class, resource_api):
        seen = set()
        lock = threading.Lock()

        def retrieve_and_deduplicate(asset_ids):
            res = resource_api.list(asset_ids=asset_ids, limit=-1)
            resources = resource_list_class([])
            with lock:
                for resource in res:
                    if resource.id not in seen:
                        resources.append(resource)
                        seen.add(resource.id)
            return resources

        ids = [a.id for a in self.data]
        tasks = []
        for i in range(0, len(ids), self._retrieve_chunk_size):
            tasks.append({"asset_ids": ids[i : i + self._retrieve_chunk_size]})
        res_list = utils._concurrency.execute_tasks_concurrently(
            retrieve_and_deduplicate, tasks, resource_api._config.max_workers
        ).results
        resources = resource_list_class([])
        for res in res_list:
            resources.extend(res)
        return resources


# GenClass: AssetFilter.filter
class AssetFilter(CogniteFilter):
    """No description.

    Args:
        name (str): Name of asset. Often referred to as tag.
        parent_ids (List[int]): Return only the direct descendants of the specified assets.
        parent_external_ids (List[str]): Return only the direct descendants of the specified assets.
        root_ids (List[Dict[str, Any]]): Only include these root assets and their descendants.
        asset_subtree_ids (List[Dict[str, Any]]): Only include assets in subtrees rooted at the specified assets (including the roots given). If the total size of the given subtrees exceeds 100,000 assets, an error will be returned.
        data_set_ids (List[int]): No description.
        metadata (Dict[str, str]): Custom, application specific metadata. String key -> String value. Limits: Key are at most 128 bytes. Values are at most 10240 bytes. Up to 256 key-value pairs. Total size is at most 10240.
        source (str): The source of this asset
        created_time (Union[Dict[str, Any], TimestampRange]): Range between two timestamps.
        last_updated_time (Union[Dict[str, Any], TimestampRange]): Range between two timestamps.
        root (bool): filtered assets are root assets or not
        external_id_prefix (str): External Id provided by client. Should be unique within the project.
        types (List[Dict[str, Any]]): No description.
        labels (List[List[Dict[str, Any]]]): A label filter is composed in the following manner: [<label> AND <label> AND ...] OR [<label> AND <label> AND ...] OR ... In the associated example, the applied filter will return all the ACTIVE PUMPs and all the VALVEs.
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self,
        name: str = None,
        parent_ids: List[int] = None,
        parent_external_ids: List[str] = None,
        root_ids: List[Dict[str, Any]] = None,
        asset_subtree_ids: List[Dict[str, Any]] = None,
        data_set_ids: List[int] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        created_time: Union[Dict[str, Any], TimestampRange] = None,
        last_updated_time: Union[Dict[str, Any], TimestampRange] = None,
        root: bool = None,
        external_id_prefix: str = None,
        types: List[Dict[str, Any]] = None,
        labels: List[List[Dict[str, Any]]] = None,
        cognite_client=None,
    ):
        self.name = name
        self.parent_ids = parent_ids
        self.parent_external_ids = parent_external_ids
        self.root_ids = root_ids
        self.asset_subtree_ids = asset_subtree_ids
        self.data_set_ids = data_set_ids
        self.metadata = metadata
        self.source = source
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.root = root
        self.external_id_prefix = external_id_prefix
        self.types = types
        self.labels = labels
        self._cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: Union[Dict, str], cognite_client=None):
        instance = super(AssetFilter, cls)._load(resource, cognite_client)
        if isinstance(resource, Dict):
            if instance.created_time is not None:
                instance.created_time = TimestampRange(**instance.created_time)
            if instance.last_updated_time is not None:
                instance.last_updated_time = TimestampRange(**instance.last_updated_time)
        return instance

    # GenStop
