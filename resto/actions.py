from typing import TypeVar

Model = TypeVar('Model')


class ActionsLoader:
    def __init__(self):
        self.connector = None

    def set_connector(self, action_connector):
        self.connector = action_connector


DefaultActions: ActionsLoader = ActionsLoader()


class ActionsConnector:
    @staticmethod
    def fetcher(
        model: type[Model],
        args: dict,
        strict_filter: dict,
        query: dict,
        projection: dict,
    ) -> Model:
        raise NotImplementedError

    @staticmethod
    def inserter(model: type[Model], data: dict) -> Model:
        raise NotImplementedError

    @staticmethod
    def updater(model: type[Model], id: str, data: dict, upsert: bool = False) -> Model:
        raise NotImplementedError

    @staticmethod
    def deleter(model: type[Model], id: str, filter: dict) -> Model:
        raise NotImplementedError
