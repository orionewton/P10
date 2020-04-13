from django.shortcuts import render, redirect, get_object_or_404
from .models import Food, Substitute
from .off_api import Api
import ast
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import re

# Create your views here.
def handler404(request, *args, **argv):
    response = render('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

def home(request):
    return render(request, 'home/home.html')
    
@login_required
def saved(request):
    sub = Substitute.objects.filter(author=request.user)
    paginator = Paginator(sub, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {
        'substitutes_saveds': sub, 'products': products
    }
    return render(request, 'home/saved.html', context)
    
class SavedListView(LoginRequiredMixin,ListView):
    model = Substitute
    template_name = 'home/saved.html'
    context_object_name = 'substitutes_saveds'
    paginate_by = 4

    def get_queryset(self):
        return Substitute.objects.filter(author=self.request.user)
        
def search(request):
    if request.method == 'POST':
        if "next" in request.POST:
            value = {}
            value['next'] = request.POST.get('next', None)
            finalvalue = ast.literal_eval(value['next'])
            categorie = a.select_categorie(finalvalue['info'][0])
            context = {'foods'    : a.get_results_from_category(categorie, finalvalue['info'][1]),
                       'firstfood': value['next']}
            return render(request, 'home/search.html', context, {'title': 'Descriptif'})
    return render(request, 'home/search.html', {'title': 'Résultats'})

def searchnova(request):
    if request.method == 'POST':
        if "next" in request.POST:
            value = {}
            value['next'] = request.POST.get('next', None)
            finalvalue = ast.literal_eval(value['next'])
            categorie = a.select_categorie(finalvalue['info'][0])
            context = {'foods'    : a.get_results_from_category_nova(categorie, finalvalue['info'][
                1]),
                       'firstfood': value['next']}
            return render(request, 'home/search.html', context, {'title': 'Descriptif'})
    return render(request, 'home/search.html', {'title': 'Résultats'})

@login_required
def confirmation(request):
    if request.method == 'POST':
        if "save" in request.POST:
            value = {}
            value['save'] = request.POST.get('save', None)
            finalvalue = ast.literal_eval(value['save'])
            newprod1 = Food(
                name=finalvalue[0]['product_name_fr'],
                url=finalvalue[0]['url'],
                url_img=finalvalue[0]['img'],
                url_nutri=finalvalue[0]['url_nutri'],
                category=finalvalue[0]['categorie'],
                stores=finalvalue[0]['stores'],
                nutriscore=finalvalue[0]['nutriletter'],
                novascore=finalvalue[0]['novascore'],
                author=request.user)

            newprod2 = Food(
                name=finalvalue[1]['product_name_fr'],
                url=finalvalue[1]['url'],
                url_img=finalvalue[1]['img'],
                url_nutri=finalvalue[1]['url_nutri'],
                category=finalvalue[1]['categorie'],
                stores=finalvalue[1]['stores'],
                nutriscore=finalvalue[1]['nutriletter'],
                novascore=finalvalue[1]['novascore'],
                author=request.user)

            newprod1.save()
            newprod2.save()
            sub = Substitute(
                urloriginal=Food.objects.filter(url=finalvalue[0]['url'])[0],
                urlsubstitute=Food.objects.filter(url=finalvalue[1]['url'])[0],
                author=request.user)
            sub.save()

            messages.success(request, f'Vos choix ont bien été enregistrés !')
            return redirect('../')

def product(request):
    value = {}
    value['info'] = request.POST.get('info', None)
    context = {
        'product': ast.literal_eval(value['info'])}
    return render(request, 'home/product.html', context, {'title': 'Descriptif'})

def infosaved(request):
    value = {}
    value['info'] = request.POST.get('info', None)
    p = Food.objects.filter(url=value['info']).first()
    context = {
        'product': p, 'stores': ast.literal_eval(al.stores)
    }
    return render(request, 'home/infosaved.html', context, {'title': 'Descriptif'})

def proposition(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            if re.search('[a-zA-Z]', query):
                results = a.get_results_from_search(query)
                print(results)
                if results:
                    context = {'foods': results}
                    return render(request, 'home/proposition.html', context,
                                  {'title': 'Proposition'})
                else:
                    context = {'message': 'noresults'}
                    return render(request, 'home/home.html', context)
            else:
                context = {'message': 'noresults'}
                return render(request, 'home/home.html', context)

@login_required
def delete(request):
    if request.method == 'POST':
        if "delete" in request.POST:
            value = {}
            value['delete'] = request.POST.get('delete', None)
            context = {
                'product': value['delete']
            }
            return render(request, 'home/delete.html', context, {'title': 'Suppression'})
            
def validatedelete(request):
    if request.method == 'POST':
        if "delete" in request.POST:
            value = {}
            value['delete'] = request.POST.get('delete', None)
            id = int(value['delete'])
            sub = Substitute.objects.get(id=id)
            sub.delete()
            messages.success(request, f'Produits supprimés !')
            return redirect('../saved/')

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Substitute
    success_url = '/saved/'

    def test_func(self):
        sub = self.get_object()
        if self.request.user == sub.author:
            return True
        return False
        
def mention(request):
    return render(request, 'home/mention.html', {'title': 'Mentions légales'})


a = Api()
