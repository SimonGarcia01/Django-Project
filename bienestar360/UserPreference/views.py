from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserPreference
from .forms import UserPreferenceForm

@login_required
def setup_preferences(request):
    preferences, created = UserPreference.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=preferences)
        if form.is_valid():
            form.save()
            return redirect('homepageUser:homepageUser')
        else:
            # If form is invalid, render the form with errors
            return render(request, 'userpreference/setup_preferences.html', {'form': form})
    else:
        form = UserPreferenceForm(instance=preferences)

    return render(request, 'userpreference/setup_preferences.html', {'form': form})
