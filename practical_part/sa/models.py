from django.db import models

# Create your models here.


class Table(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    upper_bound = models.CharField(max_length=255, default="K.a")
    lower_bound = models.CharField(max_length=255, default="K.a")


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
    start_temp = models.FloatField(default=0.0)
    reduction_rate = models.FloatField(default=0.0)
    count = models.IntegerField(default=0.0)
    count_increase = models.FloatField(default=1.2)
    sa_num = models.IntegerField(default=0)
    result_image = models.CharField(max_length=255, editable=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    
