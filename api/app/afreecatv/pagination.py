from rest_framework.pagination import LimitOffsetPagination


class AfreecaTVPagination(LimitOffsetPagination):
    default_limit = 15
