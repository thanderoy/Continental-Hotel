from django.conf import settings
from django.shortcuts import HttpResponse, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient

from .forms import ReservationForm
from .helpers import render_to_pdf
from .models import Category, Reservation, ReservationStatus, Room


def RoomOfferingView(request):
    offerings = Category.objects.all()

    context = {
        "offerings": offerings,
    }
    return render(request, "hotel/room_list.html", context)


def RoomDetailView(request, id):
    category = get_object_or_404(
        Category.objects.get(id=id))

    available_room = category.get_available_rooms().first()

    if request.method == "GET":
        form = ReservationForm()
        context = {
            "available_room": available_room,
            "form": form,
        }

        return render(request, "hotel/room_detail.html", context)

    elif request.method == "POST":
        form = ReservationForm(request.POST)

        if form.is_valid:
            form = form.cleaned_data

            reservation = Reservation.objects.create(
                owner=request.user,
                room=room,
                check_in=form.get("check_in"),
                check_out=form.get("check_out"),
                status=ReservationStatus.PENDING,
            )

            # Initiate Payment procedure
            client = MpesaClient()
            callback_url = settings.CALLBACK_URL

            response = client.stk_push(
                form.get("phone_number"),
                room.category.price,
                "The Continental.",
                "Room Reservation",
                callback_url,
            )

            response = response.json()

            context = {
                "reservation": reservation,
            }

            return render(request, "hotel/reservation_created.html", context)


def ReservationListView(request):
    if request.user.is_staff is False:
        # For non-staff users, only get their Reservations
        reservations = Reservation.objects.filter(
            owner=request.user,
        ).order_by("created")
    else:
        # For staff + superusers, get all Reservations.
        reservations = Reservation.objects.all()

    context = {
        "reservations": reservations
    }

    return render(request, "hotel/reservation_list.html", context)


def ReservationDetailView(request, id):
    reservation = get_object_or_404(
        Reservation.objects.get(
            id=id,
        )
    )

    if request.method == "POST":
        reservation.cancel()

    context = {
        "reservation": reservation
    }

    return render(request, "hotel/reservation_detail.html", context)


@csrf_exempt
def stk_push_callback(request):
    if request.method == "POST":
        data = request.body
        data = data.json()

        result_code = data.get("Body")["stkcallback"]["ResultCode"]
        result_desc = data.get("Body")["stkcallback"]["ResultDesc"]

        if result_code != "0":
            return render(request, "hotel/payment_error.html")


def ReceiptDownloadView(request, reservation: Reservation):
    if request.method == "GET":
        data = {
            "company": "The Continental.",
            "tag": "Where the wicked rest.",
            "email": "helpdesk@thecontinental.com",
            "phone": "0790906416",
            "room": reservation.room.room_number,
            "user": reservation.owner,
            "category": reservation.room.category.category_name,
        }

        receipt = render_to_pdf("receipt_template.html", data)

        response = HttpResponse(receipt, content_type="application/pdf")

        filename = f"Receipt_{reservation.room.room_number} \
            - {reservation.room.category.category_name}_{reservation.created}.pdf"
        content = f"attachment; filename={filename}"
        response["Content-Disposition"] = content
        return response
