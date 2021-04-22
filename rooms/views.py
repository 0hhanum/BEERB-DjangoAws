from django.shortcuts import render
from django.core.paginator import Paginator
from . import models

# 수동으로 pagination 만들기
# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     page = int(page or 1)  # /?page=  url 에 이렇게 입력했을 땐 값이 없어서 오류가 난다. get 기본값과는 다름.
#     page_size = 10
#     limit = page_size * page
#     offset = limit - page_size
#     all_rooms = models.Room.objects.all()[offset:limit]
#     page_count = ceil(models.Room.objects.count() / page_size)
#     return render(
#         request,
#         "rooms/home.html",
#         context={
#             "rooms": all_rooms,
#             "page": page,
#             "page_count": page_count,
#             "page_range": range(1, page_count + 1),
#         },
#     )


def all_rooms(request):
    page = int(request.GET.get("page", 1))
    room_list = models.Room.objects.all()
    # 지금이 아닌 room_list 가 호출됐을 때 query set 을 불러온다. DataBase 가 방대할 때는 치명적일 수 있으니 조심.
    paginator = Paginator(room_list, 10, orphans=5)  # 자투리 다섯개까지는 마지막 페이지로 밀어넣기
    # rooms = paginator.get_page(page)  # 10 단위로 쪼갰을 때 get 으로 얻은 page 에 해당하는 page 객체.
    rooms = paginator.page(page)
    return render(request, "rooms/home.html", context={"page": rooms})
