from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re


class SanitizedInputAPIView(APIView):
    """ This class represents a SanitizedInputAPIView. """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests, process input data, and return the appropriate response.
        """
        try:
            input_string = request.data.get('input', '')
            if not input_string:
                result = {"result": "sanitized"}
            if self.is_sanitized(input_string):
                result = {"result": "sanitized"}
            else:
                result = {"result": "unsanitized"}

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def is_sanitized(self, input_string):
        sql_injection_pattern = re.compile(r'[\;\*\|\'\"\=\(\)\[\]\{\}\%\@\,]')

        if sql_injection_pattern.search(input_string):
            return False
        return True
