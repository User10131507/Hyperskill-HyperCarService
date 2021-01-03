from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect


class WelcomeView(View):
    def get(self):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request):
        context = {'services': ['change_oil', 'inflate_tires', 'diagnostic']}
        return render(request, 'tickets/menu.html', context)


line_of_cars = {'change_oil': [], 'inflate_tires': [], 'diagnostic': []}


class Temp:
    queue = []


class TicketView(View):
    ticket_number = 1

    def get(self, request, service):
        oil = len(line_of_cars['change_oil'])
        tires = len(line_of_cars['inflate_tires'])
        dia = len(line_of_cars['diagnostic'])

        if service == 'change_oil':
            minutes_to_wait = (oil * 2)
        elif service == 'inflate_tires':
            minutes_to_wait = (oil * 2) + (tires * 5)
        else:
            minutes_to_wait = (oil * 2) + (tires * 5) + (dia * 30)

        self.ticket_number += oil + tires + dia
        line_of_cars[service].append(self.ticket_number)

        context = {'ticket_number': self.ticket_number, 'minutes_to_wait': minutes_to_wait}

        return render(request, 'tickets/ticket.html', context)


class OperatorView(View):
    first_pop = None

    def get(self, request):
        oil = len(line_of_cars['change_oil'])
        tires = len(line_of_cars['inflate_tires'])
        dia = len(line_of_cars['diagnostic'])

        context = {'oil': oil, 'tires': tires, 'dia': dia}

        return render(request, 'tickets/operator.html', context)

    def post(self, request):
        queue = Temp.queue
        if not queue:
            for line in line_of_cars:
                queue.extend(line_of_cars[line])

            for line in line_of_cars:
                if len(line_of_cars[line]) > 0:
                    self.first_pop = line_of_cars[line].pop(0)
                    break
        else:
            queue.clear()
            for line in line_of_cars:
                queue.extend(line_of_cars[line])

            for line in line_of_cars:
                if len(line_of_cars[line]) > 0:
                    line_of_cars[line].pop(0)
                    break

        return redirect('/next')


class DisplayView(View):
    def get(self, request):
        next_ticket = None
        if Temp.queue:
            next_ticket = Temp.queue[0]

        context = {'next_ticket': next_ticket}

        return render(request, 'tickets/processing.html', context)
