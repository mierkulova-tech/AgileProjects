from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from projects.models import Tag
from projects.serializers import TagSerializer
from django.shortcuts import get_object_or_404


class TagListCreateAPIView(APIView):
    def get(self, request: Request):
        tags = Tag.objects.all()
        response = TagSerializer(tags, many=True)

        return Response(data=response.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        raw_data = request.data
        data = TagSerializer(data=raw_data)
        if data.is_valid():
            data.save()

            return Response(data=data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=data.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetailApiView(APIView):
    def get(self, request: Request, pk: int):
        tag = get_object_or_404(Tag, id=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def put(self, request: Request, pk: int):
        tag = get_object_or_404(Tag, id=pk)

        serializer = TagSerializer(tag, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk: int):
        try:
            tag = Tag.objects.get(id=pk)
        except Tag.DoesNotExist:
            return Response(
                data={"message": f"Tag with id {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        tag.delete()

        return Response(
            data={"message": f"Tag with id {pk} was deleted"},
            status=status.HTTP_204_NO_CONTENT
        )
