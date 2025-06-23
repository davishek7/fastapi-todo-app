from pydantic import BaseModel


class PasswordChangeRequest(BaseModel):
    password: str
    new_password: str


class PhoneNumberUpdateRequest(BaseModel):
    new_phone_number: str