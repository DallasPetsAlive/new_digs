from typing import Any

from django.http import HttpResponse


def index(_: Any) -> HttpResponse:
    return HttpResponse("Hello, world. You're at the index.")
