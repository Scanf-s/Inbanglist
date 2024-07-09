import logging
import json

from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from chzzk.pagination import ChzzkPagination
from chzzk.serializers import ChzzkDataSerializer
from common.models import CommonModel

logger = logging.getLogger(__name__)


# 참고 링크
# https://www.django-rest-framework.org/api-guide/generic-views/#concrete-view-classes
@extend_schema(
    tags=["Chzzk"],
    summary="Retrieve a list of Chzzk streams",
    description="""
        This API endpoint retrieves a list of Chzzk streams sorted by the number of concurrent viewers in descending order.

        ## Key Features:
        - **Filtering**: Only streams from the Chzzk platform are included.
        - **Sorting**: Streams are sorted by the number of concurrent viewers in descending order, with the most viewed streams first.
        - **Pagination**: Supports pagination to handle large datasets efficiently.

        ## Response:
        The response contains a paginated list of Chzzk streams, including the following fields:
        - **id**: The unique identifier of the stream.
        - **title**: The title of the stream.
        - **concurrent_viewers**: The number of viewers currently watching the stream.
        - **platform**: The platform of the stream (always "chzzk" for this endpoint).

        ## Example:
        ```
        GET /api/v1/chzzk/

        Response:
        {
            "count": 100,
            "next": "http://example.com/api/v1/chzzk/?page=2",
            "previous": null,
            "results": [
                {
                    "id": 1,
                    "title": "Sample Stream",
                    "concurrent_viewers": 1500,
                    "platform": "chzzk"
                },
                ...
            ]
        }
        ```
    """,
)
class ChzzkListAPI(generics.ListAPIView):
    """
    API endpoint to retrieve a list of Chzzk streams sorted by the number of concurrent viewers.
    """
    serializer_class = ChzzkDataSerializer
    pagination_class = ChzzkPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CommonModel.objects.filter(platform="chzzk").order_by("-concurrent_viewers")

    def list(self, request, *args, **kwargs):
        logger.info("GET /api/v1/chzzk")

        limit = request.query_params.get('limit', ChzzkPagination.default_limit)
        offset = request.query_params.get('offset', 0)
        cache_key = f"chzzk_data_limit_{limit}_offset_{offset}"
        cache_time = 600
        data = cache.get(cache_key)

        if data is None:
            logger.info("Cache miss. Loading data from the database.")
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = serializer.data
                cache.set(cache_key, json.dumps(data), cache_time)
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data
                cache.set(cache_key, json.dumps(data), cache_time)
        else:
            logger.info("Cache hit. Loading data from the cache.")
            data = json.loads(data)

        return Response(data)


@extend_schema(
    tags=["Chzzk"],
    summary="Retrieve, update, or delete a Chzzk stream",
    description="""
        This API endpoint allows you to retrieve, update, or delete a specific Chzzk stream.

        ## Key Features:
        - **Retrieve**: Get the details of a specific Chzzk stream by its ID.
        - **Update**: Modify the details of an existing Chzzk stream. Only admin users are allowed to perform this action.
        - **Delete**: Remove a Chzzk stream from the database. Only admin users are allowed to perform this action.

        ## Authentication:
        - Requires JWT authentication. The `Authorization` header must contain a valid JWT token.

        ## Permissions:
        - Only admin users can update or delete a stream.

        ## Example:
        ### Retrieve a Stream:
        ```
        GET /api/v1/chzzk/{id}/

        Response:
        {
            "id": 1,
            "title": "Sample Stream",
            "concurrent_viewers": 1500,
            "platform": "chzzk"
        }
        ```

        ### Update a Stream:
        ```
        PUT /api/v1/chzzk/{id}/
        {
            "title": "Updated Stream Title",
            "concurrent_viewers": 2000
        }

        Response:
        {
            "id": 1,
            "title": "Updated Stream Title",
            "concurrent_viewers": 2000,
            "platform": "chzzk"
        }
        ```

        ### Delete a Stream:
        ```
        DELETE /api/v1/chzzk/{id}/

        Response:
        {
            "message": "Stream deleted successfully"
        }
        ```
    """,
)
class ChzzkRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommonModel.objects.filter(platform="chzzk")
    serializer_class = ChzzkDataSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"GET /api/v1/chzzk/{kwargs.get('pk')}")
        response = super().retrieve(request, *args, **kwargs)
        logger.info(f"Response Status Code: {response.status_code}")
        return response

    def update(self, request, *args, **kwargs):
        logger.info(f"PUT /api/v1/chzzk/{kwargs.get('pk')}")
        response = super().update(request, *args, **kwargs)
        logger.info(f"Response Status Code: {response.status_code}")
        return response

    def destroy(self, request, *args, **kwargs):
        logger.info(f"DELETE /api/v1/chzzk/{kwargs.get('pk')}")
        response = super().destroy(request, *args, **kwargs)
        logger.info(f"Response Status Code: {response.status_code}")
        return response
