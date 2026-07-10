class StorageBucketExcetion(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class RequestFaildRespones(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
