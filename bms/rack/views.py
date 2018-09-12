from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Rack_books, Rack, Book
from django.db.models import Q

# Create your views here.

class Dashboard(TemplateView):

    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        result = super(Dashboard, self).get_context_data(**kwargs)
        racks = Rack.objects.all()
        result_lst = []
        for rack in racks:
            result_lst.append({
                'rack_name': rack.name,
                'books': Rack_books.objects.filter(rack=rack.id).count(),
                'rack_id': rack.id,
            })
        result.update({
            'racks': result_lst
        })
        return result

class RackView(TemplateView):

    template_name = 'rack_page.html'

    def get_context_data(self, **kwargs):
        result = super(RackView, self).get_context_data(**kwargs)
        print(kwargs)
        result_lst = []
        rack_books = Rack_books.objects.filter(rack=kwargs['id'])
        name = ''
        for i, book in enumerate(rack_books):
            result_lst.append({
                'name': book.book.name,
                'author': book.book.author,
                'published': book.book.published
            })
            if i == 0:
                name = book.rack.name
        result.update({
            'rack_books': result_lst,
            'name': name
        })
        return result


class SearchView(TemplateView):

    template_name = 'search.html'

    def post(self, request, *args, **kwargs):
        result = {}
        search = self.request.POST.get('search')
        books = Book.objects.filter(
            Q(name__icontains=search) | Q(author__name__icontains=search) | Q(published__icontains=search))
        res_lst = []
        for book in books:
            in_rack = Rack_books.objects.filter(book=book.id)
            res_lst.append({
                'name': book.name,
                'aothor': book.author,
                'published': book.published,
                'rack': ', '.join([x.rack.name for x in in_rack])
            })
        result.update({
            'searched_res': res_lst
        })

        return render(request, self.template_name, result)

    def get_context_data(self, **kwargs):
        result = super(SearchView, self).get_context_data(**kwargs)
        return result