from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

# from django.core.paginator import Paginator
from . import models, forms

# from django.urls import reverse
# from django.http import Http404
# from django.core.paginator import Paginator, EmptyPage
# from django.utils import timezone
# from django_countries import countries


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

# Function Based View FBV
# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     # 지금이 아닌 room_list 가 호출됐을 때 query set 을 불러온다. DataBase 가 방대할 때는 치명적일 수 있으니 조심.
#     paginator = Paginator(room_list, 10, orphans=5)  # 자투리 다섯개까지는 마지막 페이지로 밀어넣기
#     # rooms = paginator.get_page(page)  # 10 단위로 쪼갰을 때 get 으로 얻은 page 에 해당하는 page 객체.
#     try:
#         rooms = paginator.page(int(page))

#         return render(request, "rooms/home.html", context={"page": rooms})

#     except EmptyPage:
#         return redirect("/")


class HomeView(ListView):  # Class Based View

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


# Function Based View

# def room_detail(request, pk):

#     try:
#         room = models.Room.objects.get(pk=pk)

#         return render(request, "rooms/detail.html", context={"room": room})

#     except models.Room.DoesNotExist:

#         # return redirect(reverse("core:home"))  # home 으로 redirect
#         raise Http404()
#         # 404 page 를 이용하면 브라우저에게도 아무것도 찾지 못했다는 걸 알려주고 저장하지 않을 수 있다.


class RoomDetail(DetailView):

    """ Room Detail Definition """

    model = models.Room


# ## Create Search View Manually
# def search(request):
#     city = request.GET.get("city", "")
#     city = str.capitalize(city)
#     country = request.GET.get("country", "KR")
#     room_type = int(request.GET.get("room_type", 0))
#     price = int(request.GET.get("price", 0))
#     guests = int(request.GET.get("guests", 0))
#     bedrooms = int(request.GET.get("bedrooms", 0))
#     beds = int(request.GET.get("beds", 0))
#     baths = int(request.GET.get("baths", 0))
#     instant = bool(request.GET.get("instant", False))
#     superhost = bool(request.GET.get("superhost", False))
#     s_amenities = request.GET.getlist("amenities")
#     s_facilities = request.GET.getlist("facilities")

#     form = {
#         "city": city,
#         "s_country": country,
#         "s_room_type": room_type,
#         "price": price,
#         "guests": guests,
#         "bedrooms": bedrooms,
#         "beds": beds,
#         "baths": baths,
#         "s_amenities": s_amenities,
#         "s_facilities": s_facilities,
#         "instant": instant,
#         "superhost": superhost,
#     }

#     room_types = models.RoomType.objects.all()
#     amenities = models.Amenity.objects.all()
#     facilities = models.Facility.objects.all()

#     choices = {
#         "countries": countries,
#         "room_types": room_types,
#         "amenities": amenities,
#         "facilities": facilities,
#     }

#     filter_args = {}

#     if city != "":
#         filter_args["city__startswith"] = city

#     filter_args["country"] = country

#     if room_type != 0:
#         filter_args["room_type__pk"] = room_type

#     if price != 0:
#         filter_args["price__lte"] = price  # less than equal

#     if guests != 0:
#         filter_args["guests__gte"] = guests

#     if bedrooms != 0:
#         filter_args["bedrooms__gte"] = bedrooms

#     if beds != 0:
#         filter_args["bed_s_gte"] = beds

#     if baths != 0:
#         filter_args["baths__gte"] = baths

#     if instant is True:
#         filter_args["instant_book"] = True

#     if superhost is True:
#         filter_args["host__superhost"] = True

#     rooms = models.Room.objects.filter(**filter_args)

#     if len(s_amenities) > 0:
#         for s_amenity in s_amenities:
#             rooms = rooms.filter(amenities__pk=int(s_amenity))

#     if len(s_facilities) > 0:
#         for s_facility in s_facilities:
#             rooms = rooms.filter(facilities__pk=s_facility)

#     return render(
#         request,
#         "rooms/search.html",
#         context={**form, **choices, "rooms": rooms},  # dict 합칠 때 unpack
#     )


class SearchView(View):
    def get(self, request):

        country = request.GET.get("country")
        city = request.GET.get("city")
        if country:
            form = forms.SearchForm(request.GET)

            # request.GET 을 통해 변수 form 에 html form 을 통해서 넘어온 정보가 저장됨.
            if form.is_valid():

                country = form.cleaned_data.get("country")
                city = form.cleaned_data.get("city")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                beds = form.cleaned_data.get("beds")
                bedrooms = form.cleaned_data.get("bedrooms")
                baths = form.cleaned_data.get("baths")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")

                filter_args = {}

                if city != "Anywhere" and city != "":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price  # less than equal

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                rooms = models.Room.objects.filter(**filter_args)

                for amenity in amenities:
                    rooms = rooms.filter(amenities=amenity)

                for facility in facilities:
                    rooms = rooms.filter(facilities=facility)
                print(rooms)
                print(filter_args)
                # paginator = Paginator(qs, 10, orphans=5)

                # page = request.GET.get("page", 1)
                # rooms = paginator.get_page(page)

        else:
            form = forms.SearchForm()
            rooms = models.Room.objects.filter(city__startswith=city)
            # return render(request, "rooms/search.html", context={"form": form})

        return render(
            request, "rooms/search.html", context={"form": form, "rooms": rooms}
        )
