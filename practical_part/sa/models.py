from django.db import models

# Create your models here.


class Table(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()


    def content_to_string(self):
        return str(self.content)


    def text_field_to_array(self):
        time_table = []
        lines = self.content_to_string().split("\n")
        for line in lines:
            job_plan = []
            job = line.strip().split(" ")
            for instance in range(0, len(job), 2):
                job_plan.append((int(job[instance]), int(job[instance + 1])))
            time_table.append(job_plan)
        return time_table
    

    def get_table_size(self):
        table = self.text_field_to_array()
        return len(table) * len(table[0])


class Result(models.Model):
    runtime = models.FloatField()
    result_length = models.IntegerField()
    result_image = models.CharField(max_length=255)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    
