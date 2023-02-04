from django.shortcuts import get_object_or_404, render
from .models import Listing
from .choices import bedroom_choices, states_choices, price_choices
from django.core.paginator import Paginator



# Create your views here.
def index (request):
    listing= Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listing,6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context={
        'listings': paged_listings,
    }
    return render(request, 'listings/listings.html',context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context={
        'listing': listing
    }
    return render(request, 'listings/listing.html')    

def search(request):

    queryset_list = Listing.objects.order_by('-list_date')
    
    if 'keywords' in request.GET:
        keywords = request.GET ['keywords']
        if keywords:
            queryset_list= queryset_list.filter(description_icontains=keywords)


    if 'city' in request.GET:
        city = request.GET ['city']
        if city:
            queryset_list= queryset_list.filter(city__iexact=city)

                   
    if 'states' in request.GET:
        states = request.GET ['states']
        if states:
            queryset_list= queryset_list.filter(description__icontains=states)

    
    if 'bedrooms' in request.GET:
        bedrooms = request.GET ['bedrooms']
        if bedrooms:
            queryset_list= queryset_list.filter(bedrooms__lte=bedrooms)


    if 'price' in request.GET:
        price = request.GET ['price']
        if price:
            queryset_list= queryset_list.filter(price__lte=price)    

    
    context = { 
    'states_choices':states_choices,
    'bedroom_choices':bedroom_choices,
    'price_choices': price_choices,
    'listings': queryset_list,
    'values': request.GET
    }
    return render(request, 'listings/search.html')   