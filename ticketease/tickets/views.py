from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Ticket
from .services import extract_ticket_data, clean_text
from accounts.models import Profile


# ---------------------------------------
# Upload / Enter Ticket Details
# ---------------------------------------
@login_required
def upload_ticket_view(request):

    if request.method == 'POST':
        try:
            # Step 1: Simulated OCR extraction
            ticket_data = extract_ticket_data(request.POST)

            # Step 2: Clean extracted text
            cleaned_text = clean_text(ticket_data["extracted_text"])

            # Step 3: Save ticket in DB
            ticket = Ticket.objects.create(
                user=request.user,
                violation_type=ticket_data["violation_type"],
                location=ticket_data["location"],
                fine_amount=ticket_data["fine_amount"],
                ticket_date=ticket_data["ticket_date"],
                extracted_text=cleaned_text,
                processed=True
            )

            messages.success(request, "Ticket processed successfully.")

            # Step 4: Redirect to prediction
            return redirect('predict_ticket', ticket_id=ticket.id)

        except Exception as e:
            messages.error(request, f"Error processing ticket: {str(e)}")
            return redirect('upload_ticket')

    return render(request, 'upload.html')


# ---------------------------------------
# View Single Ticket
# ---------------------------------------
@login_required
def ticket_detail_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    return render(request, 'result.html', {'ticket': ticket})


# ---------------------------------------
# View All Saved Cases
# ---------------------------------------
@login_required
def ticket_list_view(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'cases.html', {'tickets': tickets})


# ---------------------------------------
# Delete Ticket Case
# ---------------------------------------
@login_required
def delete_ticket_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    ticket.delete()

    messages.success(request, "Ticket deleted successfully.")
    return redirect('ticket_list')


# ---------------------------------------
# Edit Ticket (optional correction)
# ---------------------------------------
@login_required
def edit_ticket_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == 'POST':
        ticket.violation_type = request.POST.get('violation_type')
        ticket.location = request.POST.get('location')
        ticket.fine_amount = request.POST.get('fine_amount')
        ticket.ticket_date = request.POST.get('ticket_date')
        ticket.is_edited = True
        ticket.save()

        messages.success(request, "Ticket updated successfully.")
        return redirect('predict_ticket', ticket_id=ticket.id)

    return render(request, 'upload.html', {'ticket': ticket})