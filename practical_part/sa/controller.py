from .models import Table, Result


class TableController:

    def __init__(self, tables:list):
        self.tables = dict()
        for table in tables:
            self.tables[table.id] = table
    

    def get_table_size(self, table):
        return len(table) * len(table[0])


    def sort_by_table_size(self):
        sorted_tables = []
        for table in self.tables.values():
            index = 0
            while index < len(sorted_tables) and table.get_table_size() >= sorted_tables[index].get_table_size():
                index += 1
            sorted_tables.insert(index, table)
        return sorted_tables

     
    def for_table(self, table):
        head = ["job"]
        array = table.text_field_to_array()
        for i in range(len(array[0])):
            head.append(i)
        body = []
        for i, a in enumerate(array):
            new_line = []
            new_line.append(i)
            for val in a:
                new_line.append(val)
            body.append(new_line)
        return head, body
    
    def get_table_by_id(self, table_id):
        return self.tables[int(table_id)]

    
class ResultController:

    def __init__(self, tc : TableController):
        self.table_controller = tc 
    

    def get_best_solution(self, table_id):
        table = self.table_controller.get_table_by_id(id)
        results = list(table.result_set.all())
        best_result = results.pop(0)
        for r in results:
            if r.result_length < best_result.result_length:
                best_result = r
        return best_result


    def get_worst_solution(self, table_id):
        table = self.table_controller.get_table_by_id(table_id)
        results = list(table.result_set.all())
        worst_result = results.pop(0)
        for r in results:
            if r.result_length > worst_result.result_length:
                worst_result = r
        return worst_result
    

    def get_all_results(self, table_id):
        table = self.table_controller.get_table_by_id(table_id)
        results = list(table.result_set.all())
        return results
    

    def add_result(self, table_id, run_time, length,  start_temp, reduction_rate):
        table = self.table_controller.get_table_by_id(table_id)
        print(type(length))
        result = Result(runtime=run_time, result_length=length, start_temp=start_temp, reduction_rate=reduction_rate, table=table)
        result.save()
        return result.pk
    

    def delete_result(self, r):
        r.delete()

    def update_path(self, result_id, path):
        result = Result.objects.get(pk=result_id)
        result.result_image = path
        result.save()

    
