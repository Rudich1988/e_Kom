from abc import ABC


class AbstractRepository(ABC):
    def __init__(
            self,
            *args,
            **kwargs
    ) -> None:
        raise NotImplementedError

    async def get(self, data):
        raise NotImplementedError
