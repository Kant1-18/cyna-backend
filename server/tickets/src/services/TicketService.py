from tickets.models import Ticket
from tickets.src.data.repositories.TicketRepo import TicketRepo
from users.src.services.UserService import UserService


class TicketService:

    @staticmethod
    def add_ticket(user_id: int, subject: str, message: str) -> Ticket | None:
        try:
            user = UserService.get(user_id)
            if user:
                ticket = TicketRepo.add(user, subject, message)
                if ticket:
                    return ticket
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_ticket(ticket_id: int) -> Ticket | None:
        try:
            ticket = TicketRepo.get(ticket_id)
            if ticket:
                return ticket
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all_tickets_by_user(user_id: int) -> list[Ticket] | None:
        try:
            user = UserService.get(user_id)
            if user:
                tickets = TicketRepo.get_all_by_user(user)
                if tickets:
                    return tickets
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_ticket_status(ticket_id: int, status: int) -> Ticket | None:
        try:
            ticket = TicketRepo.update_status(ticket_id, status)
            if ticket:
                return ticket
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def delete_ticket(ticket_id: int) -> Ticket | None:
        try:
            ticket = TicketRepo.delete(ticket_id)
            if ticket:
                return ticket
        except Exception as e:
            print(e)

        return None
