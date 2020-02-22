from django.shortcuts import render, redirect
from user.forms import UserRegister
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from Request_Handler.Economy.create import createVenue, createDatabase
from user.models import Venue, Agents, Transaction, Economy, UserDetails, Booking
from Request_Handler.Economy.verify import verify, creditAccount, getBalance, debitUserAccount
from datetime import datetime
from Request_Handler.Economy.time import checkTime, getAmount


@login_required
def home(request):
    venue = Venue.objects.filter(status=True).order_by('id')
    booking = Booking.objects.filter(booked_by=request.user, state=True).exists()
    if booking:
        booking = Booking.objects.filter(booked_by=request.user, state=True).get()

    return render(request, 'home.html', {'venue': venue, 'balance': getBalance(request.user), 'booking': booking})


def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = UserDetails()
            user.user_id = new_user
            user.save()
            messages.success(request, f'Account Created Successfully')
            return redirect('login')
    else:
        form = UserRegister()
        return render(request, 'register.html', {'form': form})


def arduino(request):
    agents = Agents.objects.filter(id=request.GET['id']).get()
    agents.spaceStatus = request.GET['spaceStatus']
    agents.save()
    booking = Booking.objects.filter(agent=agents, state=True).get()
    if datetime.now() >= datetime.strptime(booking.endTime, '%Y-%m-%d %H:%M:%S'):
        booking.paidStatus = False
        booking.save()
        return HttpResponse('TrueFalse')
    else:
        return HttpResponse(str(agents.booked_status) + '' + str(agents.openCloseStatus))


def test(request):
    createDatabase()
    createVenue()
    return HttpResponse(True)


def agent(request):
    venue = Venue.objects.filter(id=request.GET['venue']).exists()
    if venue:
        venue = Venue.objects.filter(id=request.GET['venue'])
        agents = Agents.objects.filter(venue=request.GET['venue'])
        return render(request, 'agents.html',
                      {'agent': agents, 'venue': venue.values(), 'balance': getBalance(request.user)})
    else:
        messages.info(request, 'Please Enter A Valid Venue')
        return redirect('home')


def bookAgent(request):
    if request.method == 'GET':
        if Agents.objects.filter(id=request.GET['agentId']).exists():
            agents = Agents.objects.filter(id=request.GET['agentId']).get()
            venue = Venue.objects.filter(id=agents.venue_id).get()
            return render(request, 'book.html', {'agent': agents, 'venue': venue, 'balance': getBalance(request.user)})
        else:
            messages.warning(request, 'Please Enter A Valid Agent')
            return redirect('home')


def redeem(request):
    if request.method == 'GET':
        transactions = Transaction.objects.filter(user=request.user, type='credited').order_by('-created_at').values()
        return render(request, 'redeem.html',
                      {'transactions': transactions, 'total': len(transactions), 'balance': getBalance(request.user)})
    elif request.method == 'POST':
        check = verify(request.POST['hash'])
        if check:
            credit = creditAccount(request.user, request.POST['hash'])
            if credit:
                messages.success(request, 'Your Account Was Credited Successfully')
                return redirect('redeem')
            else:
                messages.warning(request, 'Opps Something Went Wrong')
                return redirect('redeem')
        else:
            messages.info(request, 'Invalid Hash Provided')
            return redirect('redeem')


def transaction(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at').values()
    return render(request, 'transactions.html',
                  {'balance': getBalance(request.user), 'transactions': transactions, 'total': len(transactions)})


def bookAgent(request):
    if request.method == 'POST':
        start = datetime.strptime(str(datetime.now().date()) + ':' + str(request.POST['start']), '%Y-%m-%d:%H:%M')
        end = datetime.strptime(str(datetime.now().date()) + ':' + str(request.POST['end']), '%Y-%m-%d:%H:%M')
        amount = getAmount(datetime.now(), end)
        get_balance = UserDetails.objects.filter(user_id=request.user).get()
        if get_balance.balance >= amount:
            agents = Agents.objects.filter(id=request.POST['agent']).get()
            if checkTime(start, end):
                book = Booking()
                book.agent = agents
                book.booked_by = request.user
                book.startTime = datetime.now()
                book.endTime = end
                book.paidStatus = False
                book.renew = False
                book.received = 0
                book.total_amount = amount
                book.save()
                pay = debitUserAccount(request.user, amount)
                if pay:
                    book.received = amount
                    book.paidStatus = True
                    book.save()
                    agents.booked_status = True
                    agents.save()
                    messages.success(request, 'Booking Made Successfully')
                    return redirect('home')

            else:
                messages.info(request,
                              'Make Sure That The Current Time And Booking Time Is Not More Than 25 min And Not Less Than 16 min')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            messages.info(request, 'Insufficient Balance Total Amount Was' + str(amount) + 'Your Account Has' + str(
                get_balance.balance))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def openClose(request):
    if request.method == 'POST':
        agents = Agents.objects.filter(id=request.POST['id']).get()
        if agents.openCloseStatus:
            agents.openCloseStatus = False
            agents.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            agents.openCloseStatus = True
            agents.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
