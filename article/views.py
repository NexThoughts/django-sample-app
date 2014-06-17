from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.generic.base import TemplateView
from article.models import Article
from django.http import HttpResponseRedirect
from forms import ArticleForm
from django.core.context_processors import csrf
# Create your views here.

def articles(request):
    language = 'en-us'
    session_language = 'en-us'
    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']

    if 'lang' in request.session:
        session_language = request.session['lang']

    return render_to_response('articles.html', { 'articles' : Article.objects.all(), 'language' : language, 'session_language': session_language })

def article(request, article_id = 1):
    return render_to_response('article.html', { 'article' : Article.objects.get( id=article_id) })


def language(request, language = 'en-us'):
    response = HttpResponse("setting language to %s" % language)
    response.set_cookie('lang', language)
    request.session['lang'] = language
    return response

#def hello(request):
#    name = "Mike"
#    html = "<html><body>Hi %s.</body></html>" % name
#    return  HttpResponse(html)

#def hello_template(request):
#    name = "Abhilash"
#    t = get_template('hello.html')
#    html = t.render(Context({'name' : name}))
#    return HttpResponse(html)

#def hello_template_simple(request):
#    name= "Abhishek"
#    return render_to_response('hello.html', { 'name' : name})

#class HelloTemplate(TemplateView):
#    template_name = 'hello_class.html'
#    def get_context_data(self, **kwargs):
#        context = super(HelloTemplate,self).get_context_data(**kwargs)
#        context['name']='Abhilas'
#        return context

def create(request):
    if request.POST:
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/articles/all')
        else:
            form = ArticleForm()

        args = {}
        args.update(csrf(request))

        args['form'] = form

        return render_to_response('create_article.html', args)