from django.db import models

class Member(models.Model):
    id = models.CharField(max_length = 20, primary_key = True)
    pw = models.CharField(max_length = 512)
    name = models.CharField(max_length = 11)
    nickname = models.CharField(max_length = 10)
    age = models.IntegerField()
    gender = models.BooleanField() 
    authority = models.IntegerField() 
    phonenumber = models.CharField(max_length=15)
    email = models.CharField(max_length=45)

    def get_id(self):
        return self.id

    def get_dic(self):
        return {
            'id':self.id,
            'name' : self.name,
            'nickname' : self.nickname,
            'age' : self.age,
            'gender' : '남성' if self.gender == True else '여성',
            'phonenumber' : self.phonenumber,
            'email' : self.email
        }

class SementicRecord(models.Model):
    sementic_record_id = models.AutoField(primary_key = True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add = True)
    initial_value = models.FloatField(default = 36.5)
    current_temperature = models.FloatField(default = 36.5)
    reflected_number = models.PositiveIntegerField(default = 1)

    def get_dic(self):
        return {
            'date' : self.date.strftime("%m%d"), 
            'temperature' : format(self.current_temperature,".2f")
        }