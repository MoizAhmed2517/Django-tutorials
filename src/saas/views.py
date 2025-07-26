import pathlib
from django.shortcuts import render
from django.http import HttpResponse
from visits.models import PageVisit

cwd = pathlib.Path(__file__).resolve().parent

### Inline html reponse [HTTP way]
# def home_page_view(request, *args, **kwargs):
#     return HttpResponse("<h1> Welcome to the SaaS Foundation Home Page</h1>")

# def home_page_view(request, *args, **kwargs):
#     print("cwd:", cwd)
#     html_ = cwd.joinpath("home.html").read_text()
#     return HttpResponse(html_)

# def home_page_view(request, *args, **kwargs):
#     my_title = "My SaaS App"
#     my_context = {
#         'page_title': my_title,
#         'my_content': "Welcome to the SaaS Foundation Home Page",
#     }
    
#     html_ = """
#         <!DOCTYPE html>
#         <html lang="en">
#             <body>
#                 <h1>Welcome to our {page_title}</h1>
#             </body>
#         </html>
#     """.format(**my_context)
    
    # return HttpResponse(html_)
    

### The preferred style:

# def home_page_view(request, *args, **kwargs):
#     my_title = "SaaS App"
#     my_context = {
#         'page_title': my_title,
#         'my_content': "This is the home page of the SaaS Foundation project and we are building something big!",
#     }
#     html_template = "home.html"
#     return render(request, html_template, my_context)

### Improving the template rendering with visit app

def home_page_view(request, *args, **kwargs):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)
    my_title = "SaaS App"
    my_context = {
        'page_title': my_title,
        'my_content': "This is the home page of the SaaS Foundation project and we are building something big!",
        'qs': qs,
        'page_visit_count': page_qs.count(),
        "page_visit_percentage": page_qs.count() * 100 / qs.count() if qs.count() > 0 else 0,
        "total_visits": qs.count(),
    }
    html_template = "home.html"
    PageVisit.objects.create(path=request.path)  # Log the visit
    return render(request, html_template, my_context)

def x_page_view(request, *args, **kwargs):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)
    my_title = "SaaS App"
    my_context = {
        'page_title': my_title,
        'my_content': "This is the home page of the SaaS Foundation project and we are building something big!",
        'qs': qs,
        'page_visit_count': page_qs.count(),
        "page_visit_percentage": page_qs.count() * 100 / qs.count() if qs.count() > 0 else 0,
        "total_visits": qs.count(),
    }
    html_template = "home.html"
    PageVisit.objects.create(path=request.path)  # Log the visit
    return render(request, html_template, my_context)