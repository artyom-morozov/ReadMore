import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Book, Rating, User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import RatingForm #, AddRatingForm

class SearchResultsView(ListView):
    model = Book
    template_name = 'search_results.html'
    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
        return object_list

class MyRatingsView(ListView):
    model = Rating
    template_name = 'read/ratings.html'
    context_object_name = 'ratings'
    paginate_by = 8
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyRatingsView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user).order_by('value')

# Add book rating
def add_rating(request): #, book_id, user_id):
    if request.method == "POST":
        # rating = form.cleaned_data['value']
        # book = form.cleaned_data['book']
        # da = json.load(request.POST)
        book_id = request.POST.get('book_id')
        user = request.user
        rating = request.POST.get('rating')
        print('recieved from post '+str([book_id, user, rating]))

        obj = Rating(book_id=book_id, user=user, value=rating)
        obj.save()
    return redirect('/ratings/')

def home(request):
    book_list = Book.objects.all()
    p = Paginator(book_list, 5)

    context = {
        'book_chunks': [p.get_page(i).object_list for i in p.page_range]
    }
    if request.user.is_authenticated:
        return render(request, 'read/home.html', context)
    else:
        return redirect('logout/')

# Create your views here.
# Detail view for a book
class BookDetailView(DetailView):
    model = Book

def about(request):
    return render(request, 'read/about.html')