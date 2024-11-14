from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Event, Participant
from .forms import EventForm, ParticipantForm
from django.utils import timezone

# Index (Landing Page) View
def index(request):
    return render(request, 'index.html')  # Serving index.html as the homepage

@login_required
def dashboard(request):
    events = Event.objects.filter(created_by=request.user)  # Fetch events created by the logged-in user
    return render(request, 'events/dashboard.html', {'events': events})

# List all events
def event_list(request):
    events = Event.objects.all()
    
    # Check if the user has already participated in any event
    participated_events = Participant.objects.filter(user=request.user)
    
    # Add a flag to each event if the user has already participated
    for event in events:
        event.is_participated = participated_events.filter(event=event).exists()

    return render(request, 'events/event_list.html', {'events': events})

# Event detail view
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_creator = request.user == event.created_by  # Check if the user is the creator

    # Fetch participants only if the user is the creator
    participants = event.participants.all() if is_creator else None

    return render(request, 'events/event_detail.html', {
        'event': event,
        'participants': participants,
        'is_creator': is_creator  # Pass the flag to the template
    })

# Create a new event
@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)  # Ensure request.FILES is passed here
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user  # Set the logged-in user as the creator
            event.save()
            return redirect('dashboard')  # Redirect to dashboard after successful event creation
        else:
            print("Form errors:", form.errors)  # Debugging to check if there are any form errors
    else:
        form = EventForm()
    return render(request, 'events/event_create.html', {'form': form})

# Update an existing event
@login_required
def event_update(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)  # Make sure to handle file upload
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)  # Redirect to event detail page after saving
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_edit.html', {'form': form, 'event': event})

# Delete an event
@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the logged-in user is the creator of the event
    if request.user != event.created_by:
        messages.error(request, "You do not have permission to delete this event.")
        return redirect('event_detail', event_id=event.id)  # Redirect to event detail page if no permission

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('dashboard')  # Redirect to dashboard after deletion

    return render(request, 'events/event_confirm_delete.html', {'event': event})

# User login view
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('dashboard')  # Redirect to dashboard after successful login
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'events/login.html', {'form': form})


# User logout view
@login_required
def logout_user(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

# Dashboard view (show events for the logged-in user)
@login_required
def dashboard(request):
    events = Event.objects.filter(created_by=request.user)  # Show only the events created by the logged-in user
    return render(request, 'events/dashboard.html', {'events': events})

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            messages.success(request, 'Registration successful.')
            return redirect('dashboard')  # Redirect to dashboard after registration
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'events/register.html', {'form': form})


@login_required
def register_participant(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the user is already registered for this event
    if Participant.objects.filter(user=request.user, event=event).exists():
        messages.info(request, "You are already registered for this event!")
        return redirect('event_list')  # Redirect to event list page if already registered

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            user = request.user
            phone_number = form.cleaned_data['phone_number']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            # Register the participant
            Participant.objects.create(
                user=user,
                event=event,
                name=name,
                email=email,
                phone_number=phone_number
            )
            messages.success(request, "You have successfully registered for the event!")
            return redirect('event_list')  # Redirect to event list after successful registration
        else:
            messages.error(request, "There was an error with the form. Please try again.")
    else:
        form = ParticipantForm()

    return render(request, 'events/register_participant.html', {'form': form, 'event': event})
