from dataclasses import dataclass


@dataclass
class PermissionMixin:
    def get_permissions_by_action(
        self, permission_classes_by_action: dict, action, permission_classes
    ):
        try:
            return [permission() for permission in permission_classes_by_action[action]]
        except KeyError:
            return [permission() for permission in permission_classes]
