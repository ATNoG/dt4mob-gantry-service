from pydantic import BaseModel, NonNegativeInt


class DittoSettings(BaseModel):
    toll_id: NonNegativeInt = 0
    namespace: str = "default"
    subject: str = "test"
    policy_id: str = "default:policy"
