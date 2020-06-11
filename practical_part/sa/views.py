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


def sa(request, id):
    if request.method == "GET":
        print(id)
        table = Table.objects.get(pk=id)
        t_controller = TableController(list(Table.objects.all()))
        r_controller = ResultController(t_controller)
        run_simmulated_annealing(str(table.content), id, table.name, r_controller)
        return "succes"  
