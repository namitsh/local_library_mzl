from datetime import date, timedelta

from django.shortcuts import render, HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404,reverse

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required, permission_required

from catalog.models import Book, BookInstance, Author, Genre

from .forms import RenewBookForm

# Create your views here.


def index(request):
    ''' View function for home page of site '''

    # generate counts of objects
    books = Book.objects.all().count()
    book_instances = BookInstance.objects.all().count()
    authors = Author.objects.count()

    # num of visites
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # available books in the library
    num_instances_available = BookInstance.objects.filter(availability__exact='a').count()
    biography_books = Book.objects.filter(genre__name__icontains='biography').count()

    context = {
        'num_books' : books,
        'num_books_instances' : book_instances,
        'num_authors' : authors,
        'num_instances_available': num_instances_available,
        'biography_books': biography_books,
        'num_visits': num_visits
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    queryset = Book.objects.all()[:5]
    template_name = 'books/book_list.html'
    context_object_name =  'my_book_list'
    paginate_by = 10


    # alternate of queryset
    # def get_queryset(self):
    #     return Book.objects.all()[:5]

    # if we want to add more context in the data with list of books

    # def get_context_data(self, **kwargs):
    #     # call the base implementation , to get the context
    #     context = super(BookListView,self).get_context_data(**kwargs)
    #     # create any data and add it to context
    #     context[data] = 'some data'
    #     return context




# function based view (fbv) of book-detail
@login_required
def book_detail_view(request,pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', context={ 'book': book })


# OR CBV 

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'




def author_list_view(request):
    authors = Author.objects.all()
    return render(request, 'authors/author_list.html' , context ={ 'author_list': authors})


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'authors/author_detail.html'


class LoanedByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'book_instance/list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(availability__exact='o').order_by('due_back')



class LoanedByAllUsersListView(PermissionRequiredMixin, generic.ListView ):
    
    model = BookInstance
    permission_required = 'catalog.can_marked_returned'
    
    paginate_by = 10
    template_name = 'book_instance/list_borrowed_all.html'

    def get_queryset(self):
        return BookInstance.objects.filter(availability__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_marked_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_ins = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_ins.due_back = form.cleaned_data['renewal_date']
            book_ins.save()

            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = date.today() + timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        
    context ={
        'form' : form,
        'book_ins' : book_ins
    }

    return render(request, 'books/book_renew_librarian.html' , context)


class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__'

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')


class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('author-list')
