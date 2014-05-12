from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from django_gravatar.helpers import get_gravatar_url, has_gravatar

from .forms import FilterMemberForm
from accounts.models import Profile
from skills.models import UserSkill


@login_required
def dashboard(request):
    """
    Shows all members as a list - with the capacity to filter by
    member skills and preferences.
    """
    # Get additional profile data
    user = request.user

    #~working_offline = False
    working_offline = True

    if not working_offline:
        user.gravatar_exists = has_gravatar(user.email)

    # Display members
    listed_members = User.objects.filter(is_active=True).order_by('first_name')

    if request.method == 'POST':
        form = FilterMemberForm(request.POST)
        if form.is_valid():
            skills = form.cleaned_data['selected_skills']
            preferences = form.cleaned_data['selected_preferences']

            if skills:
                listed_members = listed_members.filter(
                                                skill__in=skills).distinct()
            if preferences:
                listed_members = listed_members.filter(
                    profile__connect_preferences__in=preferences).distinct()
    else:
        form = FilterMemberForm()

    context = {
        'user' : user,
        'listed_members': listed_members,
        'form': form,
    }

    return render(request, 'discover/list.html', context)


@login_required
def map(request):
    """
    Shows all members on a world map.
    """
    return render(request, 'discover/map.html')


