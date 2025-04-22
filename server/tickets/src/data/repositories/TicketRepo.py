from tickets.models import Ticket
from users.models import User


class TicketRepo:

    @staticmethod
    def add(user: User, subject: str, message: str) -> Ticket | None:
        try:
            ticket = Ticket.objects.create(user=user, subject=subject, message=message)
            if ticket:
                return ticket
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get(id: int) -> Ticket | None:
        try:
            ticket = Ticket.get(id=id)
            if ticket:
                return ticket
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_by_user_and_status(user: User, status: int) -> Ticket | None:
        try:
            ticket = Ticket.objects.get(user=user, status=status)
            if ticket:
                return ticket
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_all_by_user(user: User) -> list[Ticket]:
        try:
            tickets = Ticket.objects.filter(user=user)
            if tickets:
                return tickets
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update_status(ticket_id: int, status: int) -> Ticket | None:
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.status = status
            ticket.save()
            return ticket
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def delete(ticket_id: int) -> Ticket | None:
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.delete()
            return ticket
        except Exception as e:
            print(e)
            return None
