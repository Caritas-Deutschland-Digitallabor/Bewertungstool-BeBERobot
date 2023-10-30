from django.db import models
from cms.models import CMSPlugin
from polls.models import Poll
import datetime

# Table in SQL to save the workshops associated with each user
class Workshop(models.Model):
    user_name = models.CharField(max_length=50)
    workshop_id = models.CharField(max_length=50, unique=True)
    workshop_name = models.CharField(max_length=100)
    workshop_date = models.DateField(default=datetime.date.today)

# Table in SQL to save the roles required in each setting
class RolesLang(models.Model):
    role_id = models.CharField(max_length=10) # Write it like Lang+number
    role_name = models.CharField(max_length=50)
    mandatory = models.BooleanField(default=False)

class RolesAku(models.Model):
    role_id = models.CharField(max_length=10) # Write it like Aku+number
    role_name = models.CharField(max_length=50)
    mandatory = models.BooleanField(default=False)

class RolesAmbu(models.Model):
    role_id = models.CharField(max_length=10) # Write it like Ambu+number
    role_name = models.CharField(max_length=50)
    mandatory = models.BooleanField(default=False)

# Table in SQL to save the setting of the workshop
class Setting(models.Model):
    workshop_id = models.CharField(max_length=10, blank=False)
    setting = models.CharField(max_length=50, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    robot_name = models.CharField(max_length=100, blank=True)

# Table in SQL to save the roles and name of the participants of the workshop
class Roles(models.Model):
    workshop_id = models.CharField(max_length=10, blank=False)
    role_id = models.CharField(max_length=10, default='0000000')
    role = models.CharField(max_length=100, blank=True)
    names = models.CharField(max_length=400, blank=True)

# Table in SQL for questions of the langzeitstationär setting
class LangPoll(models.Model):
    # Each one of this is one of the columns of the table 
    ques_id = models.IntegerField(default=0)
    economy = models.CharField(max_length=400, blank=True)
    care = models.CharField(max_length=400, blank=True)
    technology  = models.CharField(max_length=400, blank=True)
    embedding = models.CharField(max_length=400, blank=True)
    law = models.CharField(max_length=400, blank=True)
    ethics = models.CharField(max_length=400, blank=True)

# Table in SQL for mouse effect of each question of the langzeitstationär setting
class LangMouse(models.Model):
    # Each one of this is one of the columns of the table 
    ques_id = models.IntegerField(default=0)
    economy = models.CharField(max_length=2000, blank=True)
    care = models.CharField(max_length=2000, blank=True)
    technology  = models.CharField(max_length=2000, blank=True)
    embedding = models.CharField(max_length=2000, blank=True)
    law = models.CharField(max_length=2000, blank=True)
    ethics = models.CharField(max_length=2000, blank=True)

# Table in SQL to save the answers of the langzeitstationär setting
class LangPoll_Answer(models.Model):
    # Each one of this is one of the columns of the table 
    question = models.CharField(max_length=400, blank=True)
    choice = models.CharField(max_length=20, blank=True)
    comment = models.CharField(max_length=1000, blank=True)
    comment_unless = models.CharField(max_length=1000, blank=True)
    skipped = models.BooleanField(default=False)
    ques_id = models.IntegerField(default=0)
    category = models.CharField(max_length=50, blank=True)
    workshop_id = models.CharField(max_length=10, blank=False)

# Table in SQL for questions of the akutstationär setting
class AkuPoll(models.Model):
    # Each one of this is one of the columns of the table 
    ques_id = models.IntegerField(default=0)
    economy = models.CharField(max_length=400, blank=True)
    care = models.CharField(max_length=400, blank=True)
    technology  = models.CharField(max_length=400, blank=True)
    embedding = models.CharField(max_length=400, blank=True)
    law = models.CharField(max_length=400, blank=True)
    ethics = models.CharField(max_length=400, blank=True)

# Table in SQL for mouse effect of each question of the akutstationär setting
class AkuMouse(models.Model):
    # Each one of this is one of the columns of the table 
    ques_id = models.IntegerField(default=0)
    economy = models.CharField(max_length=2000, blank=True)
    care = models.CharField(max_length=2000, blank=True)
    technology  = models.CharField(max_length=2000, blank=True)
    embedding = models.CharField(max_length=2000, blank=True)
    law = models.CharField(max_length=2000, blank=True)
    ethics = models.CharField(max_length=2000, blank=True)

# Table in SQL to save the answers of the akutstationär setting
class AkuPoll_Answer(models.Model):
    # Each one of this is one of the columns of the table 
    # ID = model.IntegerField
    question = models.CharField(max_length=400, blank=True)
    choice = models.CharField(max_length=20, blank=True)
    comment = models.CharField(max_length=1000, blank=True)
    comment_unless = models.CharField(max_length=1000, blank=True)
    skipped = models.BooleanField(default=False)
    ques_id = models.IntegerField(default=0)
    category = models.CharField(max_length=50, blank=True)
    workshop_id = models.CharField(max_length=10, blank=False)

# Table in SQL for questions of the ambulant setting
class AmbuPoll(models.Model):
    # Each one of this is one of the columns of the table 
    ques_id = models.IntegerField(default=0)
    economy = models.CharField(max_length=400, blank=True)
    care = models.CharField(max_length=400, blank=True)
    technology  = models.CharField(max_length=400, blank=True)
    embedding = models.CharField(max_length=400, blank=True)
    law = models.CharField(max_length=400, blank=True)
    ethics = models.CharField(max_length=400, blank=True)

# Table in SQL for mouse effect of each question of the ambulant setting
class AmbuMouse(models.Model):
    # Each one of this is one of the columns of the table 
    ques_id = models.IntegerField(default=0)
    economy = models.CharField(max_length=2000, blank=True)
    care = models.CharField(max_length=2000, blank=True)
    technology  = models.CharField(max_length=2000, blank=True)
    embedding = models.CharField(max_length=2000, blank=True)
    law = models.CharField(max_length=2000, blank=True)
    ethics = models.CharField(max_length=2000, blank=True)

# Table in SQL to save the answers of the ambulant setting
class AmbuPoll_Answer(models.Model):
    # Each one of this is one of the columns of the table 
    question = models.CharField(max_length=400, blank=True)
    choice = models.CharField(max_length=20, blank=True)
    comment = models.CharField(max_length=1000, blank=True)
    comment_unless = models.CharField(max_length=1000, blank=True)
    skipped = models.BooleanField(default=False)
    ques_id = models.IntegerField(default=0)
    category = models.CharField(max_length=50, blank=True)
    workshop_id = models.CharField(max_length=10, blank=False)
