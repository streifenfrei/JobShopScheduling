from django.shortcuts import render
from django.http import HttpResponse
from .models import Table, Result
from .controller import TableController, ResultController
from django.http import JsonResponse
from django.template.loader import render_to_string
from .simulated_annealing import run_simmulated_annealing

# Create your views here.
def index(request):
    return render(request, "html/index.html")
    
        
def run(request):
    if request.method == 'GET':
        tables = Table.objects.all()
        controller = TableController(list(tables))
        tables = controller.sort_by_table_size()
        table = controller.get_table_by_id(tables[0].id)
        head, body = controller.for_table(table)
        context = { 'tables' : tables, 'body' : body, 'head' : head,}
        return render(request=request, template_name="html/run.html", context=context)

def change_table(request , id):
    tables = Table.objects.all()
    controller = TableController(list(tables))
    tables = controller.sort_by_table_size()
    table = controller.get_table_by_id(int(id))
    head, body = controller.for_table(table)
    context = {  'body' : body, 'head' : head,}
    data = {'content' : render_to_string(template_name="html/table.html", context=context)}
    return JsonResponse(data)


def sa(request, id, temp, r_rate, count):
    if request.method == "GET":
        table = Table.objects.get(pk=id)
        t_controller = TableController(list(Table.objects.all()))
        r_controller = ResultController(t_controller)
        result_id = run_simmulated_annealing(str(table.content), id, table.name, r_controller, temp=float(temp), reduction_rate=float(r_rate), count=int(count))
        result = Result.objects.get(pk=result_id)
        if result_id is not None:
            data = {'success' : 1, 'source' : "static/" + result.result_image, 'result_length' : result.result_length, 'runtime' : result.runtime}
        else:
            data = {'success' : 1, 'source' : "No new result", 'result_length' : "No new result", 'runtime' :  "No new result"}
        return JsonResponse(data)


def show_results(request):
    tables = Table.objects.all()
    controller = TableController(list(tables))
    sorted_tables = controller.sort_by_table_size()
    result_controller = ResultController(controller)
    table = controller.get_table_by_id(sorted_tables[0].id)
    results = result_controller.get_all_results(table.id)
    context = {'tables' : sorted_tables, 'results' : results}
    return render(request=request, template_name="html/results.html", context=context)


def filter_results(request, id):
    if request.method == "GET":
        table = Table.objects.get(pk=id)
        t_controller = TableController(list(Table.objects.all()))
        r_controller = ResultController(t_controller)
        results = r_controller.get_all_results(table.id)
        context = {'results' : results}
        data = {'content' : render_to_string(template_name="html/result_table.html", context=context)}
        return JsonResponse(data)


def show_schedule(request, id):
    result = Result.objects.get(pk=id)
    src = "static/" + result.result_image
    data = {'source' : src}
    return JsonResponse(data)
