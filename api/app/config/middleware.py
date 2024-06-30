import logging

logger = logging.getLogger("django.request")


class RequestResponseLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 정적 파일 요청을 필터링
        if not request.path.startswith("/static/"):
            # 요청 로깅
            logger.info(f"Request Method: {request.method}, Path: {request.get_full_path()}")

        response = self.get_response(request)

        # 정적 파일 요청을 필터링
        if not request.path.startswith("/static/"):
            # 응답 로깅
            logger.info(f"Response Status Code: {response.status_code}")

        return response
