from commons.deidentifications import pi_cipher, pi_masker


class DeidentificationMixin:
    @property
    def masked_username(self):
        return pi_masker.mask_name(self.decrypted_username)

    @property
    def masked_email(self):
        return pi_masker.mask_email(self.decrypted_email)

    @property
    def masked_phone(self):
        return pi_masker.mask_phone(self.decrypted_phone)

    @property
    def masked_detail_address(self):
        return pi_masker.generic_mask(self.decrypted_detail_address)

    @property
    def masked_detail_shipping_address(self):
        return pi_masker.generic_mask(self.decrypted_detail_shipping_address)

    @property
    def decrypted_username(self):
        return pi_cipher.decrypt(self.username)

    @property
    def decrypted_email(self):
        return pi_cipher.decrypt(self.email)

    @property
    def decrypted_phone(self):
        return pi_cipher.decrypt(self.phone)

    @property
    def decrypted_detail_address(self):
        return pi_cipher.decrypt(self.detail_address)

    @property
    def decrypted_detail_shipping_address(self):
        return pi_cipher.decrypt(self.detail_shipping_address)

    @property
    def encrypted_username(self):
        return pi_cipher.encrypt(self.username)

    @property
    def encrypted_email(self):
        return pi_cipher.encrypt(self.email)

    @property
    def encrypted_phone(self):
        return pi_cipher.encrypt(self.phone)

    @property
    def encrypted_detail_address(self):
        return pi_cipher.encrypt(self.detail_address)

    @property
    def encrypted_detail_shipping_address(self):
        return pi_cipher.encrypt(self.detail_shipping_address)
