from tickets.models import Ticket
from tickets.src.services.TicketService import TicketService
from users.src.services.AuthService import AuthService
from ninja.errors import HttpError
from utils.CheckInfos import CheckInfos


class TicketControl:

    @staticmethod
    def add(request, data) -> Ticket | HttpError:
        try:
            if not CheckInfos.is_valid_string(data.subject):
                return HttpError(400, "Invalid string for subject")

            if not CheckInfos.is_valid_string(data.message):
                return HttpError(400, "Invalid string for message")

            token = AuthService.get_access_token(request)
            user = AuthService.get_user_by_access_token(token)

            ticket = TicketService.add_ticket(user.id, data.subject, data.message)
            if ticket:
                return ticket.to_json()
        except Exception as e:
            print(e)
            raise HttpError(500, "An error occurred while adding the ticket")

    @staticmethod
    def get(id: int) -> Ticket | HttpError:
        try:
            ticket = TicketService.get_ticket(id)
            if ticket:
                return ticket.to_json()
            else:
                raise HttpError(404, "Ticket not found")
        except Exception as e:
            print(e)
            raise HttpError(500, "An error occurred while getting the ticket")

    @staticmethod
    def get_all_by_user(request) -> list[Ticket] | HttpError:
        try:
            token = AuthService.get_access_token(request)
            user = AuthService.get_user_by_access_token(token)
            tickets = TicketService.get_all_tickets_by_user(user.id)
            if tickets:
                return [ticket.to_json() for ticket in tickets]
            else:
                raise HttpError(404, "No tickets found")
        except Exception as e:
            print(e)
            raise HttpError(500, "An error occurred while getting all tickets")

    @staticmethod
    def update_status(request, data) -> Ticket | HttpError:
        try:
            if not CheckInfos.is_positive_int(data.ticketId):
                return HttpError(400, "Invalid id")

            if not CheckInfos.is_status_ticket(data.status):
                return HttpError(400, "Invalid status")

            token = TicketService.update_ticket_status(data.ticketId, data.status)
            if token:
                return token.to_json()
            else:
                raise HttpError(404, "Ticket not found")
        except Exception as e:
            print(e)
            raise HttpError(500, "An error occurred while updating the ticket status")

    @staticmethod
    def delete(request, id: int) -> Ticket | HttpError:
        try:
            token = TicketService.delete_ticket(id)
            if token:
                return token.to_json()
            else:
                raise HttpError(404, "Ticket not found")
        except Exception as e:
            print(e)
            raise HttpError(500, "An error occurred while deleting the ticket")
