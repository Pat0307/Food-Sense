from django.shortcuts import render, redirect
from .models import Profile, Favorite
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required

def profile(request):
    try:
        userProfile = Profile.objects.get(user=request.user)
        return render(request, 'users/profile.html', {"profile": userProfile})
    except Profile.DoesNotExist:
        return redirect("users:createProfile")

@login_required
def createProfile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('users:profile')
    else:
        form = ProfileForm()
        predefined_diseases=["Diabetes"]
        predefined_allergies=["Peanut Allergy"]
        return render(request, "users/profileform.html", {"form": form, 'predefined_diseases': predefined_diseases, 'predefined_allergies': predefined_allergies})

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.diseases = [
                disease for disease in request.POST.getlist('diseases') if disease
            ]
            profile.allergies = [
                allergy for allergy in request.POST.getlist('allergies') if allergy
            ]
            profile.save()
            return redirect('users:profile')
    else:
        form=ProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {"form": form, "profile": profile})

@login_required
def favorites_list(request):
    return render(request, 'users/favorite_list.html')
@login_required
def favorite(request, id):
    item = Favorite.objects.get(id=id)
    return render(request, 'users/favorite.html', {"item": item})

@login_required
def delete_favorite(request):
    if request.method == 'POST':
        favorite_id = request.GET.get('favorite_id')
        try:
            favorite = Favorite.objects.get(pk=favorite_id)
            favorite.delete()
            return JsonResponse({'success': True})
        except Favorite.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'favorite not found.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})