from tickets.models import Ticket
from tickets.src.controllers.TicketControl import TicketControl
from ninja import Router, ModelSchema, Schema
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

router = Router()


class TicketSchema(ModelSchema):
    class Meta:
        model = Ticket
        fields = "__all__"


class TicketAddSchema(Schema):
    subject: str
    message: str


class TicketUpdateSchema(Schema):
    ticketId: int
    status: int


@router.post("/add", auth=JWTAuth())
def add(request, data: TicketAddSchema) -> Ticket | HttpError:
    return TicketControl.add(request, data)


@router.get("/get/{id}", auth=JWTAuth())
def get(request, id: int) -> Ticket | HttpError:
    return TicketControl.get(id)


@router.get("/get-all-my", auth=JWTAuth())
def get_all_my(request) -> list[Ticket] | HttpError:
    return TicketControl.get_all_my(request)


@router.get("/get-all-by-user/{id}", auth=JWTAuth())
def get_all_by_user(request, id: int) -> list[Ticket] | HttpError:
    return TicketControl.get_all_by_user(request, id)


@router.patch("/update-status", auth=JWTAuth())
def update_status(request, data: TicketUpdateSchema) -> Ticket | HttpError:
    return TicketControl.update_status(request, data)


@router.delete("/delete/{id}", auth=JWTAuth())
def delete(request, id: int) -> Ticket | HttpError:
    return TicketControl.delete(request, id)
