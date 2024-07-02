import logging
import os
import random
import string

from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from s3.S3Instance import S3Instance
from s3.serializers import UploadProfileImageSerializer
from users.models import User

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["S3"],
    summary="사용자 프로필 이미지 업로드",
    description="""
    This API endpoint Uploads a profile image for the authenticated user.
    
    Steps:
        1. Retrieve the authenticated user from the request.
        2. Check if the 'profile_image' file is present in the request.
        3. If not, return a response with an error message and a status code of 400.
        4. Generate a random string of 16 characters to use as the image name.
        5. Construct the image name using the user ID and the random string.
        6. Create an S3 client instance.
        7. Upload the file to the S3 bucket using the S3 client.
        8. Construct the URL of the uploaded image.
        9. Update the user's profile image with the URL.
        10. Save the user.
        11. Return a response with the URL of the uploaded image.
        12. If there is an exception during the upload process, return a response with the error message and a status code of 400.
    """,
    request={"multipart/form-data": UploadProfileImageSerializer},
    responses={200: UploadProfileImageSerializer, 400: "파일이 제공되지 않음 또는 업로드 과정에서 오류 발생"},
)
class UploadProfileImageView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UploadProfileImageSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        """
        Uploads a profile image for the authenticated user.
        """

        logger.info("PUT /api/v1/users/profile_image/upload")
        user = self.request.user
        if "profile_image" not in request.FILES:
            logger.error("No file provided")
            return Response({"error": "No file provided"}, status=400)

        file = request.FILES["profile_image"]
        s3_client = S3Instance().get_s3_instance()
        random_string = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        profile_image_name = f"profile_images/{user.id}/{random_string}.png"

        if user.profile_image:  # 이전 프로필 이미지 삭제
            old_image_key = user.profile_image.split(f"https://{os.getenv('AWS_S3_BUCKET_NAME')}.s3.amazonaws.com/")[-1]
            try:
                s3_client.delete_object(Bucket=os.getenv("AWS_S3_BUCKET_NAME"), Key=old_image_key)
            except Exception as e:
                logger.error(f"Failed to delete old image: {str(e)}")
                return Response({"error": f"Failed to delete old image: {str(e)}"}, status=400)

        try:
            s3_client.upload_fileobj(
                file,
                os.getenv("AWS_S3_BUCKET_NAME"),
                profile_image_name,
            )
            profile_image_url = f"https://{os.getenv('AWS_S3_BUCKET_NAME')}.s3.amazonaws.com/{profile_image_name}"
            user.profile_image = profile_image_url
            user.save()
            logger.info(f"Profile image uploaded successfully for user {user.id}")
            return Response({"profile_image": profile_image_url})
        except Exception as e:
            logger.error(f"Failed to upload image: {str(e)}")
            return Response({"error": str(e)}, status=400)
