from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    # Default rute that loads the index function in views.py
    path('', views.IndexView, name='index'),
    # Rute to the sign up page
    path("register/", views.register, name='register'),
    # Rute to activation page after confirming the email
    path('activate/<slug:uidb64>/<slug:token>/',views.activate, name='activate'),
    # Rute to the log in page
    path("login_user/", views.login_user, name="login_user"),
    # Rute to the log out page
    path("logout_user/", views.logout_user, name="logout_user"),
    # Rute to the show the users register to delete page
    path("show_delete_user/", views.show_delete_user, name="show_delete_user"),
    # Rute to the delete user page
    path("delete_user/", views.delete_user, name="delete_user"),
    # Rute to reset the password
    path("password_reset/", views.password_reset_request, name="password_reset"),
    # Rute to the list of workshops page
    path("list_workshop/", views.list_workshop, name="list_workshop"),
    # Rute to the creation of workshops page
    path("create_workshop/", views.create_workshop, name="create_workshop"),
    # Rute to save the workshops page
    path("save_workshop/", views.save_workshop, name="save_workshop"),
    # Rute to introduction page
    path('intro/', views.intro, name='intro'),
    # Rute to first page for defining setting and participants
    path('setting/', views.setting_view, name='setting'),
    # Rute to first page for saving setting and participants
    path('save_setting/', views.save_setting, name='save_setting'),
    # Rute to page with questions 
    path('questions/<str:category>/<int:question_id>/', views.question_view, name='questions'), 
    # Rute to function that goes from one question to another 
    path('questions/<str:category>/<int:question_id>/next_ques/', views.next_ques, name='next_ques'),
    # Rute to function that goes from one question to previous 
    path('questions/<str:category>/<int:question_id>/prev_ques_lang/', views.prev_ques_lang, name='prev_ques_lang'),
    # Rute to function that skip one question
    path('questions/<str:category>/<int:question_id>/skip_ques/', views.skip_ques, name='skip_ques'),
    # Rute to function that shows skipped question
    path('questions/show_skip_ques/', views.show_skip_ques, name='show_skip_ques'), 
    # Rute to function that shows  the next skipped question
    path('questions/next_skip_ques/<str:category>/<int:question_id>/', views.next_skip_ques, name='next_skip_ques'),
    # Rute to skip a question inside the skipped question section
    path('questions/skip_skip_ques/', views.skip_skip_ques, name='skip_skip_ques'),
    # Rute to evaluation page
    path('evaluation/', views.evaluation, name='evaluation'),
    # Rute to create and download PDF page
    path('create_pdf/', views.create_pdf, name='create_pdf'),

    

]
