from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from rest_framework import viewsets
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q


class AuthenticationView(viewsets.ViewSet):
    def sign_in_user(self, request: HttpRequest):
        if request.method == "POST":
            try:
                username = request.POST["username"]
                password = request.POST["password"]
                if User.objects.filter(
                    Q(username=username) & Q(password=password)
                ).exists():
                    return HttpResponse({"errors": ["user already exist"]}, status=400)
                elif User.objects.filter(username=username).exists():
                    return HttpResponse({"errors": ["bad password"]}, status=400)
                else:
                    User.objects.create_user(username=username, password=password)
                    return HttpResponse(
                        {"user": {f"{username} is authenticated"}}, status=200
                    )
            except KeyError:
                return HttpResponseBadRequest()

    def login_user(self, request: HttpRequest):
        if request.method == "POST":
            try:
                username = request.POST["username"]
                password = request.POST["password"]
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return JsonResponse(
                        {"user": f"{username} authenticated"}, status=200
                    )
                return JsonResponse(
                    {"user": f"{username} not authenticated"}, status=400
                )
            except KeyError:
                return HttpResponseBadRequest()

    def logout_user(self, request: HttpRequest):
        logout(request)
        return HttpResponse("logout", status=200)
