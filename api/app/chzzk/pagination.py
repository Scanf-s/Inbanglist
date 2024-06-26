from rest_framework.pagination import LimitOffsetPagination

class ChzzkPagination(LimitOffsetPagination):
    default_limit = 15