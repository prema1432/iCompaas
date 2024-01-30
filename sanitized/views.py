import re

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class SanitizedInputAPIView(APIView):
    """This class represents a SanitizedInputAPIView."""

    def post(self, request):
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
        except Exception as e:  # pylint: disable=W0718
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def is_sanitized(self, input_string):
        """Return True if the input string is sanitized, False otherwise."""
        sql_injection_pattern = re.compile(r'[\;\*\|\'\"\=\(\)\[\]\{\}\%\@\,]')

        if sql_injection_pattern.search(input_string):
            return False
        return True
