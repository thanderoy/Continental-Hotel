from typing import Any, Dict

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient

from .helpers import render_to_pdf
from .models import Reservation, Room


def RoomListView(request):
    available_rooms = Room.object.filter(
        is_reserved=False,
    )

    context = {
        "available_rooms": available_rooms,
    }
    return render(request, "room_list.html", context)


def RoomDetailView(request, room_number):
    room = get_object_or_404(Room.object.get(room_number=room_number))

    if request.method == "GET":
        form = ReservationForm()
        context = {
            "room": room,
            "form": form,
        }

        return render(request, "room_detail.html", context)

    elif request.method == "POST":
        form = ReservationForm(request.POST)

        if form.is_valid:
            form = form.cleaned_data

            reservation = Reservation.objects.create(
                owner=request.user,
                room=room,
                check_in=form.get("check_in"),
                check_out=form.get("check_out"),
                status="PENDING",
            )

            # Initiate Payment procedure
            client = MpesaClient()
            callback_url = settings.CALLBACK_URL

            response = client.stk_push(
                form.get("phone_number"),
                room.price,
                "The Continental.",
                "Room Reservation",
                callback_url,
            )

            response = response.json()

            context = {
                "reservation": reservation,
            }

            return render(request, "reservation_created.html", context)


def ReservationListView(request):
    if request.user.is_staff:
        reservations = Reservation.object.filter(
            owner=request.user,
        ).order_by("created")
    else:
        reservations = Reservation.object.all()

    context = {"reservations": reservations}

    return render(request, "reservation_list.html", context)


def ReservationDetailView(request, id):
    reservation = get_object_or_404(
        Reservation.objects.get(
            id=id,
        )
    )

    if request.method == "POST":
        reservation.cancel()
        context = {"reservation": reservation}

    return render(request, "reservation_detail.html", context)


@csrf_exempt
def stk_push_callback(request):
    if request.method == "POST":
        data = request.body
        data = data.json()

        result_code = data.get("Body")["stkcallback"]["ResultCode"]
        result_desc = data.get("Body")["stkcallback"]["ResultDesc"]

        if result_code != "0":
            return render(request, "payment_error.html")


def ReceiptDownloadView(request, reservation: Reservation):
    if request.method == "GET":
        data = {
            "company": "The Continental.",
            "tag": "Where the wicked rest.",
            "email": "helpdesk@thecontinental.com",
            "phone": "0790906416",
            "room": reservation.room,
            "user": reservation.owner,
            "category": reservation.room.category,
        }

        receipt = render_to_pdf("receipt_template.html", data)

        response = HttpResponse(receipt, content_type="application/pdf")

        filename = f"Receipt_{123124}.pdf"
        content = f"attachment; filename={filename}"
        response["Content-Disposition"] = content
        return response
