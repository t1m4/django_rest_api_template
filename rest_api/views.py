import asyncio

# Create your views here.
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import classonlymethod, method_decorator
from django.views import View
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_api.serializers import UserSerializer
from rest_api.tools import get_object_or_none


class AsyncMixin:
    """Provides async view compatible support for DRF Views and ViewSets.

    This must be the first inherited class.

        class MyViewSet(AsyncMixin, GenericViewSet):
            pass
    """

    @classmethod
    def as_view(cls, *args, **initkwargs):
        """Make Django process the view as an async view.
        """
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

        # view = super().as_view(**initkwargs)
        # async def async_view(*args, **kwargs):
        #     # wait for the `dispatch` method
        #     return await view(*args, **kwargs)
        # async_view.csrf_exempt = True
        # return async_view

    async def dispatch(self, request, *args, **kwargs):
        """Add async support.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

        try:
            await sync_to_async(self.initial)(
                request, *args, **kwargs)  # MODIFIED HERE

            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            # accept both async and sync handlers
            # built-in handlers are sync handlers
            if not asyncio.iscoroutinefunction(handler):  # MODIFIED HERE
                handler = sync_to_async(handler)  # MODIFIED HERE
            response = await handler(request, *args, **kwargs)  # MODIFIED HERE

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(
            request, response, *args, **kwargs)
        return self.response


class AsyncView(View):
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view


# TODO how to make rest api async
class UserAsyncView(AsyncView):
    async def get(self, request, *args, **kwargs):
        users = sync_to_async(User.objects.all)()
        serializer = UserSerializer(users, many=True)
        data = await self.get_data(serializer, users)
        # return JsonResponse(data, status=200, safe=False)
        # return HttpResponse(serializer.data, status=200)
        return HttpResponse("ok", status=200)
        # return Response(serializer.data, status=200)

    @sync_to_async()
    def get_data(self, ser, *args, **kwargs):
        return 'ok'

    async def post(self, request, *args, **kwargs):
        pass


class UserView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            size = int(request.GET.get('size'))
        except:
            size = 10
        size = 10 if size > 10 else size
        users = User.objects.all()[0:size]
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    def get(self, request, id, *args, **kwargs):
        user = get_object_or_none(User, id=id)
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, id, *args, **kwargs):
        user = get_object_or_none(User, id=id)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        user = get_object_or_none(User, id=id)
        if user:
            user.delete()
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)