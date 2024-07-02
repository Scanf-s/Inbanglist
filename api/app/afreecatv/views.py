import logging

from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from afreecatv.pagination import AfreecaTVPagination
from afreecatv.serializers import AfreecaTvDataSerializer
from common.models import CommonModel

# 참고 링크
# https://www.django-rest-framework.org/api-guide/generic-views/#concrete-view-classes

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["AfreecaTV"],
    summary="Retrieve a list of AfreecaTV streams",
    description="""
        This API endpoint retrieves a list of AfreecaTV streams sorted by the number of concurrent viewers in descending order.

        ## Key Features:
        - **Filtering**: Only streams from the AfreecaTV platform are included.
        - **Sorting**: Streams are sorted by the number of concurrent viewers in descending order, with the most viewed streams first.
        - **Pagination**: Supports pagination to handle large datasets efficiently.

        ## Response:
        The response contains a paginated list of AfreecaTV streams, including the following fields:
        - **id**: The unique identifier of the stream.
        - **title**: The title of the stream.
        - **concurrent_viewers**: The number of viewers currently watching the stream.
        - **platform**: The platform of the stream (always "afreecatv" for this endpoint).

        ## Example:
        ```
        GET /api/v1/afreecatv/

        Response:
        {
            "count": 100,
            "next": "http://example.com/api/v1/afreecatv/?page=2",
            "previous": null,
            "results": [
                {
                    "id": 1,
                    "title": "Sample Stream",
                    "concurrent_viewers": 1500,
                    "platform": "afreecatv"
                },
                ...
            ]
        }
        ```
    """,
)
class AfreecaTvListAPI(generics.ListAPIView):
    """
    API endpoint to retrieve a list of AfreecaTV streams sorted by the number of concurrent viewers.
    """

    queryset = CommonModel.objects.filter(platform="afreecatv").order_by("-concurrent_viewers")
    serializer_class = AfreecaTvDataSerializer
    pagination_class = AfreecaTVPagination
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve AfreecaTV streams.
        Logs the request and response status for monitoring and debugging purposes.
        """
        logger.info("GET /api/v1/afreecatv")
        response = super().list(request, *args, **kwargs)
        logger.info(f"Response Status Code: {response.status_code}")
        return response


@extend_schema(
    tags=["AfreecaTV"],
    summary="Retrieve, update, or delete an AfreecaTV stream",
    description="""
        This API endpoint allows you to retrieve, update, or delete a specific AfreecaTV stream.

        ## Key Features:
        - **Retrieve**: Get the details of a specific AfreecaTV stream by its ID.
        - **Update**: Modify the details of an existing AfreecaTV stream. Only admin users are allowed to perform this action.
        - **Delete**: Remove an AfreecaTV stream from the database. Only admin users are allowed to perform this action.

        ## Authentication:
        - Requires JWT authentication. The `Authorization` header must contain a valid JWT token.

        ## Permissions:
        - Only admin users can update or delete a stream.

        ## Example:
        ### Retrieve a Stream:
        ```
        GET /api/v1/afreecatv/{id}/

        Response:
        {
            "id": 1,
            "title": "Sample Stream",
            "concurrent_viewers": 1500,
            "platform": "afreecatv"
        }
        ```

        ### Update a Stream:
        ```
        PUT /api/v1/afreecatv/{id}/
        {
            "title": "Updated Stream Title",
            "concurrent_viewers": 2000
        }

        Response:
        {
            "id": 1,
            "title": "Updated Stream Title",
            "concurrent_viewers": 2000,
            "platform": "afreecatv"
        }
        ```

        ### Delete a Stream:
        ```
        DELETE /api/v1/afreecatv/{id}/

        Response:
        {
            "message": "Stream deleted successfully"
        }
        ```
    """,
)
class AfreecaTvRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a specific AfreecaTV stream.
    Only admin users are allowed to update or delete streams.
    """

    queryset = CommonModel.objects.filter(platform="afreecatv")
    serializer_class = AfreecaTvDataSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"GET /api/v1/afreecatv/{kwargs.get('pk')}")
        response = super().retrieve(request, *args, **kwargs)
        logger.info(f"Response Status Code: {response.status_code}")
        return response

    def update(self, request, *args, **kwargs):
        logger.info(f"PUT /api/v1/afreecatv/{kwargs.get('pk')}")
        response = super().update(request, *args, **kwargs)
        logger.info(f"Response Status Code: {response.status_code}")
        return response

    def destroy(self, request, *args, **kwargs):
        logger.info(f"DELETE /api/v1/afreecatv/{kwargs.get('pk')}")
        response = super().destroy(request, *args, **kwargs)
        logger.info(f"Response Status Code: {response.status_code}")
        return response
