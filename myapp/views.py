from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Spot, WindCondition, Review
from django.utils import timezone
from django.contrib.auth import logout
from django.views.generic import TemplateView

# Create your views here.

def spot_list(request):
    spots = Spot.objects.all()
    return render(request, 'myapp/spot_list.html', {'spots': spots})

def spot_detail(request, pk):
    spot = get_object_or_404(Spot, pk=pk)
    conditions = WindCondition.objects.filter(spot=spot).order_by('-date')[:5]
    reviews = Review.objects.filter(spot=spot).order_by('-created_at')
    return render(request, 'myapp/spot_detail.html', {
        'spot': spot,
        'conditions': conditions,
        'reviews': reviews
    })

@login_required
def add_review(request, pk):
    spot = get_object_or_404(Spot, pk=pk)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(
            spot=spot,
            user=request.user,
            rating=rating,
            comment=comment
        )
    return redirect('myapp:spot_detail', pk=pk)

@login_required
def add_condition(request, pk):
    spot = get_object_or_404(Spot, pk=pk)
    if request.method == 'POST':
        WindCondition.objects.create(
            spot=spot,
            date=timezone.now().date(),
            wind_speed=request.POST.get('wind_speed'),
            wind_direction=request.POST.get('wind_direction'),
            temperature=request.POST.get('temperature')
        )
    return redirect('myapp:spot_detail', pk=pk)

def about(request):
    
    return render(request, 'myapp/about.html')


class CustomLogoutView(TemplateView):
    template_name = 'registration/logged_out.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return super().get(request, *args, **kwargs)