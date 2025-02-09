from fastapi import HTTPException

class InsufficientFundsException(HTTPException):
    def __init__(self, detail: str = "Insufficient funds", status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)
