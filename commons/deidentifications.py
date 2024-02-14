import hashlib
from typing import Optional

from cryptography.fernet import Fernet
from django.conf import settings


class PersonalInfoCipher:
    def __init__(self):
        self.fernet = Fernet(settings.PERSONAL_INFO_FERNET_KEY)

    def encrypt(self, plain_text: str | bytes) -> Optional[bytes]:
        if not plain_text:
            return None

        if isinstance(plain_text, str):
            plain_text = plain_text.encode("utf-8")

        return self.fernet.encrypt(plain_text)

    def decrypt(self, encrypted_text: str | bytes) -> Optional[str]:
        if not encrypted_text:
            return None

        if isinstance(encrypted_text, str) and encrypted_text[0] == "b":
            encrypted_text = encrypted_text[2:-1]
        return self.fernet.decrypt(encrypted_text).decode("utf-8")


class PersonalInfoMasker:
    def __init__(self, masker="*"):
        self.masker = masker

    def mask_email(self, email) -> Optional[str]:
        if not email:
            return None
        address, domain = email.split("@")
        return f"{address[0]}{self.masker * len(address[2:])}{address[-1]}@{domain}"

    def mask_name(self, name: str) -> Optional[str]:
        if not name:
            return None
        masker = self.masker * (len(name) - 2)
        if not masker:
            return f"{name[0]}*"
        return f"{name[0]}{masker}{name[-1]}"

    def mask_phone(self, phone: str) -> Optional[str]:
        if not phone:
            return None
        phone = phone.replace("-", "")

        first_idx = 8 if len(phone) == 11 else 7
        first_number, last_number = phone[:-first_idx], phone[-4:]
        masker = self.masker * len(phone[-8:-4])

        return f"{first_number}{masker}{last_number}"

    def generic_mask(self, text: str, start: int = 1, end: int = -1):
        if not text:
            return None
        if end == -1:
            end = len(text) - 1
        return f"{text[:start]}{self.masker * (end - start)}{text[end:]}"


class PersonalInfoHasher:
    def hashed_data(self, value: str) -> Optional[bytes]:
        if value:
            return hashlib.new("sha256", value.encode("utf-8")).digest()
        else:
            return None


pi_hasher = PersonalInfoHasher()
pi_cipher = PersonalInfoCipher()
pi_masker = PersonalInfoMasker()
