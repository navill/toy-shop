from typing import Optional

from django.contrib.auth import get_user_model
from pydantic import BaseModel

from commons.deidentifications import pi_cipher, pi_hasher

User = get_user_model()


class UserDTO(BaseModel):
    ci: Optional[bytes] = None
    email: Optional[bytes] = None
    hashed_email: Optional[bytes] = None
    password: Optional[str] = None
    username: Optional[bytes] = None
    nickname: Optional[str] = None
    phone: Optional[bytes] = None

    address: Optional[str] = None
    detail_address: Optional[bytes] = None
    shipping_address: Optional[str] = None
    detail_shipping_address: Optional[bytes] = None


class UserService:
    def join(self, dto: UserDTO) -> User:
        return User.objects.create_user(
            ci=dto.ci,
            email=dto.email,
            hashed_email=dto.hashed_email,
            password=dto.password,
            username=dto.username,
            phone=dto.phone,
            nickname=dto.nickname,
            address=dto.address,
            detail_address=dto.detail_address,
            shipping_address=dto.shipping_address,
            detail_shipping_address=dto.detail_shipping_address
        )

    def update(self, user: User, dto: UserDTO) -> User:
        for field, value in dto.dict(exclude_none=True).items():
            setattr(user, field, value)
        user.save()
        return user

    def get_user_dto(self, **validated_data) -> UserDTO:
        email = validated_data.get("email")
        email = self.normalize_email(email.lower()) if email else None

        return UserDTO(
            ci=self._get_ci_from_external_api(validated_data.get("phone")),
            email=pi_cipher.encrypt(email),
            hashed_email=pi_hasher.hashed_data(email),
            password=validated_data.get("password"),
            username=pi_cipher.encrypt(validated_data.get("username")),
            phone=pi_cipher.encrypt(validated_data.get("phone")),
            nickname=validated_data.get("nickname"),

            address=validated_data.get("address"),
            detail_address=pi_cipher.encrypt(validated_data.get("detail_address")),
            shipping_address=validated_data.get("shipping_address"),
            detail_shipping_address=pi_cipher.encrypt(validated_data.get("detail_shipping_address")),
        )

    def _get_ci_from_external_api(self, phone: str) -> Optional[bytes]:
        # 회원가입 중간에 인증 기관으로부터 휴대폰 인증을 통해 ci를 받았다고 가정
        if phone:
            return pi_hasher.hashed_data(phone)
        else:
            return None

    def normalize_email(self, email: str) -> str:
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part.lower()
        return email


user_service = UserService()
