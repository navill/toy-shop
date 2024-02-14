import typing

from drf_spectacular.openapi import AutoSchema


class CustomAutoSchema(AutoSchema):
    def get_override_parameters(self) -> list:
        if hasattr(self.view, "get_param_serializer_class"):
            return [self.view.get_param_serializer_class()]
        return super().get_override_parameters()

    def get_response_serializers(self) -> typing.Any:
        # context = build_serializer_context(view)

        if hasattr(self.view, "response_serializer_class"):
            return self.view.get_response_serializer_class()
        else:
            if default_request_serializer := super().get_response_serializers():
                return default_request_serializer

    def get_request_serializer(self) -> typing.Any:
        # context = build_serializer_context(view)

        if hasattr(self.view, "request_serializer_class"):
            return self.view.get_request_serializer_class()
        else:
            if default_request_serializer := super().get_request_serializer():
                return default_request_serializer
