from django.shortcuts import render
from .query import query
from django.http import JsonResponse
from django.views import View
from django.template.loader import render_to_string
# Create your views here.



def search_view(request):
    ctx = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        songs =  query(url_parameter,10)
    else:
        songs = None

    ctx["results"] = songs
    if request.is_ajax():

        html = render_to_string(
            template_name="results_partial.html", context={"results": songs}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)
    return render(request, "results.html", context=ctx)
