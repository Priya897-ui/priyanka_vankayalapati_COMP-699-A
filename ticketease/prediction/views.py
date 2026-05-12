from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from tickets.models import Ticket
from accounts.models import Profile

from .models import Prediction
from .ml_model import get_prediction
from .utils import calculate_risk_index, generate_recommendation, generate_explanation
from tickets.services import prepare_features


# ---------------------------------------
# Predict Ticket Outcome
# ---------------------------------------
@login_required
def predict_ticket_view(request, ticket_id):

    # Step 1: Get ticket
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    # Step 2: Get driver profile
    profile = get_object_or_404(Profile, user=request.user)

    # Step 3: Prepare features
    features = prepare_features(
        {
            "violation_type": ticket.violation_type,
            "fine_amount": ticket.fine_amount
        },
        profile
    )

    # Step 4: ML Prediction
    success_probability = get_prediction(features)

    # Step 5: Risk Index
    risk_index = calculate_risk_index(features)

    # Step 6: Recommendation
    recommendation = generate_recommendation(success_probability, risk_index)

    # Step 7: Explanation
    explanation = generate_explanation(success_probability, risk_index, features)

    # ✅ Step 8: FIXED (IMPORTANT)
    prediction, created = Prediction.objects.update_or_create(
        ticket=ticket,
        defaults={
            'success_probability': success_probability,
            'risk_index': risk_index,
            'recommendation': recommendation,
            'explanation': explanation
        }
    )

    # Step 9: Update Ticket (optional but useful)
    ticket.success_probability = success_probability
    ticket.risk_index = risk_index
    ticket.recommendation = recommendation
    ticket.save()

    # Step 10: Render result page
    context = {
        'ticket': ticket,
        'prediction': prediction
    }

    return render(request, 'result.html', context)


# ---------------------------------------
# Compare Two Tickets
# ---------------------------------------
@login_required
def compare_tickets_view(request):

    tickets = Ticket.objects.filter(user=request.user)

    if request.method == 'POST':
        ticket1_id = request.POST.get('ticket1')
        ticket2_id = request.POST.get('ticket2')

        ticket1 = get_object_or_404(Ticket, id=ticket1_id, user=request.user)
        ticket2 = get_object_or_404(Ticket, id=ticket2_id, user=request.user)

        context = {
            'ticket1': ticket1,
            'ticket2': ticket2
        }

        return render(request, 'cases.html', context)

    return render(request, 'cases.html', {'tickets': tickets})