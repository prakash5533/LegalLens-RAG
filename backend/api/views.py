from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Document
from .serializers import DocumentSerializer

class DocumentUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        title = request.data.get('title', file_obj.name if file_obj else 'Untitled Document')

        if not file_obj:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        doc = Document.objects.create(
            title=title,
            file=file_obj
        )

        return Response(DocumentSerializer(doc).data, status=status.HTTP_201_CREATED)