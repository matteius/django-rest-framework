from django.test import TestCase

from rest_framework import generics, permissions
from rest_framework import schemas
from rest_framework.response import Response


class ExampleListView(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        # Mock actually using models
        response_list = [
            {'id': '1'},
            {'id': '2'},
            {'id': '3'},
        ]
        return Response(response_list)


class ExampleRetrieveView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = None

    def retrieve(self, request, *args, **kwargs):
        # Mock: do something based on request state
        data = {'request.user': "A Description of the known request object."}
        return Response(data)


class TestIsListViewLogic(TestCase):

    def test_when_view_is_retrieve_view(self):
        view = ExampleRetrieveView.as_view()
        view_url = '^my-profile/?$'

        is_list = schemas.is_list_view(view_url, 'get', view)
        self.assertFalse(is_list, "Expected a standard RetrieveAPIView to be singular lookup.")

    def test_when_view_is_list_view(self):
        view = ExampleListView.as_view()
        view_url = '^my-list/?$'

        is_list = schemas.is_list_view(view_url, 'get', view)
        self.assertTrue(is_list, "Expected a standard ListAPIView to return list data.")
