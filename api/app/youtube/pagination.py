from rest_framework.pagination import LimitOffsetPagination

class YoutubePagination(LimitOffsetPagination):
    default_limit = 15