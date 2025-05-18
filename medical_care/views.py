from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from .models import (
    EmergencyCondition, AssessmentStep, AssessmentChoice,
    PatientStatus, CPRTimer
)
from taggit.models import Tag


def index(request):
    context = {
        'emergency_list': EmergencyCondition.objects.filter(is_active=True),
        'all_tags': Tag.objects.all(),
    }
    return render(request, 'medical_care/index.html', context)


def get_info_medical_care(request, emergency_slug):
    emergency = get_object_or_404(EmergencyCondition, slug=emergency_slug)
    context = {
        'emergency': emergency,
        'emergency_list': EmergencyCondition.objects.filter(is_active=True),
        'all_tags': Tag.objects.all(),
    }
    return render(request, 'medical_care/info_medical_care.html', context)


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = EmergencyCondition.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'posts': posts,
        'emergency_list': EmergencyCondition.objects.filter(is_active=True),
        'all_tags': Tag.objects.all(),
    }
    return render(request, 'medical_care/tagged.html', context)


def post_detail(request, pk):
    post = get_object_or_404(EmergencyCondition, pk=pk)
    context = {
        'post': post,
        'emergency_list': EmergencyCondition.objects.filter(is_active=True),
        'all_tags': Tag.objects.all(),
    }
    return render(request, 'medical_care/post_detail.html', context)


def patient_assessment(request):
    emergency = EmergencyCondition.objects.filter(is_active=True).first()
    if not emergency:
        return redirect('medical_care:index')
    first_step = AssessmentStep.objects.filter(emergency=emergency).order_by('order').first()
    if first_step:
        return redirect('medical_care:assessment_step', step_id=first_step.id)
    return redirect('medical_care:index')


def patient_assessment_step(request, step_id):
    step = get_object_or_404(AssessmentStep, id=step_id)
    session_key = request.session.session_key or request.session.create()
    patient_status, _ = PatientStatus.objects.get_or_create(
        session_key=request.session.session_key,
        emergency=step.emergency
    )

    if request.method == 'POST':
        answer = request.POST.get('answer')
        choice_id = request.POST.get('choice')

        if step.question_type == 'binary':
            next_step = step.yes_next if answer == 'yes' else step.no_next
            if step.status_field:
                setattr(patient_status, step.status_field, answer == 'yes')
                patient_status.save()
        else:
            selected_choice = get_object_or_404(AssessmentChoice, id=choice_id)
            next_step = selected_choice.next_step

        if next_step:
            return redirect('medical_care:assessment_step', step_id=next_step.id)
        return redirect('medical_care:assessment_result')

    progress = 100 * (step.order / step.emergency.steps.count())

    return render(request, 'medical_care/assessment_step.html', {
        'step': step,
        'progress': progress,
        'emergency_list': EmergencyCondition.objects.filter(is_active=True),
        'all_tags': Tag.objects.all(),
    })


def assessment_result(request):
    session_key = request.session.session_key
    status = PatientStatus.objects.filter(session_key=session_key).order_by('-created_at').first()
    return render(request, 'medical_care/assessment_result.html', {
        'status': status,
        'emergency_list': EmergencyCondition.objects.filter(is_active=True),
        'all_tags': Tag.objects.all(),
    })


def cpr_timer_view(request):
    return render(request, 'medical_care/cpr_timer.html', {
        'emergency_list': EmergencyCondition.objects.filter(is_active=True),
        'all_tags': Tag.objects.all(),
    })

def call_ambulance(request):
    return render(request, 'medical_care/call_ambulance.html')

