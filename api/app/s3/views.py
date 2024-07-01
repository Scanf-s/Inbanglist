import os

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from users.models import User
from s3.serializers import UploadProfileImageSerializer
from s3.S3Instance import S3Instance
import random
import string

@extend_schema(
    tags=["S3"],
    summary="사용자 프로필 이미지 업로드",
    description="""
    인증된 사용자의 프로필 이미지를 업로드합니다.

    코드 흐름:
    1. 요청에서 인증된 사용자 정보를 가져옵니다.
    2. 요청에 'profile_image' 파일이 포함되어 있는지 확인합니다.
    3. 포함되어 있지 않으면 오류 메시지와 상태 코드 400을 반환합니다.
    4. 이미지 이름으로 사용할 16자리 랜덤 문자열을 생성합니다.
    5. 사용자 ID와 랜덤 문자열을 사용하여 이미지 이름을 구성합니다.
    6. S3 클라이언트 인스턴스를 생성합니다.
    7. S3 버킷에 파일을 업로드합니다.
    8. 업로드된 이미지의 URL을 생성합니다.
    9. 사용자의 프로필 이미지를 해당 URL로 업데이트합니다.
    10. 사용자를 저장합니다.
    11. 업로드된 이미지의 URL을 포함한 응답을 반환합니다.
    12. 업로드 과정에서 예외가 발생하면 오류 메시지와 상태 코드 400을 반환합니다.
    """,
    request={"multipart/form-data": UploadProfileImageSerializer},
    responses={
        200: UploadProfileImageSerializer,
        400: "파일이 제공되지 않음 또는 업로드 과정에서 오류 발생"
    }
)
class UploadProfileImageView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UploadProfileImageSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        """
        Uploads a profile image for the authenticated user.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A response object containing the URL of the uploaded profile image if successful,
            or an error message if there was an issue with the file or the upload process.

        Raises:
            None

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
        """

        user = self.request.user
        if 'profile_image' not in request.FILES:
            return Response({"error": "No file provided"}, status=400)
        file = request.FILES["profile_image"]
        s3_client = S3Instance().get_s3_instance()
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        profile_image_name = f"profile_images/{user.id}/{random_string}.png"

        if user.profile_image:         # 이전 프로필 이미지 삭제
            old_image_key = user.profile_image.split(f"https://{os.getenv('AWS_S3_BUCKET_NAME')}.s3.amazonaws.com/")[-1]
            try:
                s3_client.delete_object(Bucket=os.getenv("AWS_S3_BUCKET_NAME"), Key=old_image_key)
            except Exception as e:
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
            return Response({"profile_image": profile_image_url})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
