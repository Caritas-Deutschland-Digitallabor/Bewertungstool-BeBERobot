from django.contrib import messages
from django.shortcuts import render, redirect
from django.middleware import csrf

# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.utils.crypto import get_random_string

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse
from .models import  * 
from .tokens import account_activation_token

from django.contrib.sessions.backends.db import SessionStore

import datetime

# Generation PDF file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4 
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER 
from reportlab.lib import colors
from .printing import MyPrint
from io import BytesIO


def IndexView(request):
    return render(request, 'polls/welcome.html')

def register(request):
    # Get the values of all the fields
    if request.method == 'POST':
        last_name = request.POST['last_name'] # We have only one field for the name, where both first and last name are written 
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        context = {}

        # Check if the passwords match and then if the user or email already exit
        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                context["last_name"] = last_name
                context["email"] = email
                context["password"] = password
                messages.info(request, 'Benutzername ist bereits vergeben')
                return render(request, 'polls/registration.html', context)

            elif User.objects.filter(email=email).exists():
                context["last_name"] = last_name
                context["username"] = username
                context["password"] = password
                messages.info(request, 'E-Mail ist bereits vergeben')
                return render(request, 'polls/registration.html', context)

            else: # If everything is new we create and save the new user
                try:
                    validate_password(password)
                    print ("VALID PASSWORD", flush=True)
                    user = User.objects.create_user(username=username, password=password, 
                                            email=email, last_name=last_name) 
                    user.is_active = False # Deactivate account till it is confirmed
                    user.save()

                    current_site = get_current_site(request)
                    subject = 'Activate Your Ready? Account'
                    message = render_to_string('confirmation_email/account_activation_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })

                    email_conf = EmailMessage(
                        subject, message, to=[email]
                    )

                    email_conf.send()
                    return redirect ("/email_sent/")
                    
                except ValidationError as e:
                    messages.error(request, str(e))
                    context["last_name"] = last_name
                    context["username"] = username
                    context["email"] = email
                    return render(request, 'polls/registration.html', context)
                    
                
        else:
            context["last_name"] = last_name
            context["username"] = username
            context["email"] = email
            messages.info(request, 'Beide Passwörter stimmen nicht überein')
            return render(request, 'polls/registration.html', context)
            

    else:
        return render(request, 'polls/registration.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect ("/email_confirmed/")
    else:
        return redirect ("/link_invalid/")


def login_user(request):
    # Get values from fields
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if the values match a user 
        user = auth.authenticate(username=username, password=password)

        if user is not None: # If they match we move forward on the page
            auth.login(request, user)
            return redirect('polls:list_workshop')
        
        else: # If not we redirect again to the login
            messages.info(request, 'Ungültiger Benutzername oder Passwort')
            return redirect('polls:login_user')
    else:
        return render(request, 'polls/login.html')

def logout_user(request):
    auth.logout(request)
    return redirect('polls:login_user')

def show_delete_user(request):
    Users = User.objects.filter(is_staff=False)
    # for user in Users: 
    workshop_list = Workshop.objects.all()
    return render(request, "polls/delete_user.html", {
        "Users": Users, 
        "WorkshopList": workshop_list
    })
    
def delete_user(request):
    print ("USER DELETED")

    if request.method == 'POST':
        selected_user = request.POST.get("user_id", "")
        password = request.POST['password']

        # Check if the values match a user 
        user = auth.authenticate(username=selected_user, password=password)

        if user is not None: # If they match we move forward on the page

            # Delete all the workshop associated with that user
            workshop_list = Workshop.objects.filter(user_name=selected_user)
            for workshop in workshop_list:
                try:
                    selected_setting = get_object_or_404(Setting, workshop_id=workshop.workshop_id)
                    selected_workshop = get_object_or_404(Workshop, workshop_id=workshop.workshop_id)
                    saved_roles = Roles.objects.filter(workshop_id=workshop.workshop_id)
                    langpoll_answered_ques = LangPoll_Answer.objects.filter(workshop_id=workshop.workshop_id)
                    akupoll_answered_ques = AkuPoll_Answer.objects.filter(workshop_id=workshop.workshop_id)
                    ambupoll_answered_ques = AmbuPoll_Answer.objects.filter(workshop_id=workshop.workshop_id)

                    selected_setting.delete()
                    print ("DELETED SETTING", flush=True)
                    saved_roles.delete()
                    print("DELETED ROLES")
                    langpoll_answered_ques.delete()
                    print("DELETED LANGPOLL ANSWERS", flush=True)
                    akupoll_answered_ques.delete()
                    print("DELETED AKUPOLL ANSWERS", flush=True)
                    ambupoll_answered_ques.delete()
                    print("DELETED AMBUPOLL ANSWERS", flush=True)
                    selected_workshop.delete()
                    print("WORKSHOP IS DELETED")
               
                except:
                    selected_workshop = get_object_or_404(Workshop, workshop_id=workshop.workshop_id)
                    selected_workshop.delete()
                    print("WORKSHOP IS DELETED")
               
            # Delete the user
            u = User.objects.get(username = selected_user)
            u.delete()

            return redirect('polls:login_user')
        else: # If not we redirect again to the delete user page
            messages.info(request, 'Ungültiger Passwort')
            return redirect('polls:show_delete_user')

    else:
        return redirect('polls:show_delete_user')


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(email=data) 
			if associated_users.exists():
				for user in associated_users:
					subject = "Passwortrücksetzung angefordert"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'localhost:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'pflegeundrobotik@gmx.de' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Ungültiger Header gefunden.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

@login_required(login_url='polls:login_user')
def list_workshop(request): # Get the workshops associated with the logged in user
    username = request.user.username
    workshop_list = Workshop.objects.filter(user_name=username)
    print ("USER: ", username, flush=True)
    return render(request, "polls/list_workshop.html", {
        "WorkshopList": workshop_list
    })

@login_required(login_url='polls:login_user')
def create_workshop(request):
    today_date = datetime.date.today()
    print(today_date, flush=True)
    return render(request, 'polls/create_workshop.html',{
        "today_date": today_date.isoformat()
    })


@login_required(login_url='polls:login_user')
def save_workshop(request):
    username = request.user.username
    name_workshop = request.POST.get("text_name_workshop", "")
    date_workshop = request.POST.get("date_workshop", "")
    id_workshop = get_random_string(5)
    
    # Save data into the workshop database related with the user
    workshop_saved = Workshop(user_name = username, workshop_id = id_workshop, workshop_name = name_workshop, workshop_date = date_workshop)
    workshop_saved.save()
    return redirect('polls:list_workshop')

@login_required(login_url='polls:login_user')
def intro(request):
    if 'intro_workshop' in request.POST:
        workshop_id = request.POST.get("workshop_id", "")
        request.session['workshop_id'] = workshop_id
        print("WORKSHOP ID: ", workshop_id, flush=True) 
        
        if not Setting.objects.filter(workshop_id = workshop_id).exists(): # If there is no workshop started with that id we start the workshop from the beggining
            return render(request, "polls/intro.html")
        else: # If the workshop was started we load the last not answered question
            print ("WORKSHOP WAS ALREADY STARTED")
            # 1) Obtain the total number of questions, the total number of questions answered and skipped
            n_ques_total = 0    
            selected_setting = get_object_or_404(Setting, workshop_id=workshop_id)

            if selected_setting.setting == "langzeitstationär":
                skipped_ques_t = LangPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
                ques_answered_total = LangPoll_Answer.objects.filter(workshop_id=workshop_id)
                n_ques_answered_total = LangPoll_Answer.objects.filter(workshop_id=workshop_id).count()
                question_economy = LangPoll.objects.values_list("economy", flat=True)
                question_care = LangPoll.objects.values_list("care", flat=True)
                question_technology = LangPoll.objects.values_list("technology", flat=True)
                question_embedding = LangPoll.objects.values_list("embedding", flat=True)
                question_law = LangPoll.objects.values_list("law", flat=True)
                question_ethics = LangPoll.objects.values_list("ethics", flat=True)

            elif selected_setting.setting == "akutstationär":
                skipped_ques_t = AkuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
                ques_answered_total = AkuPoll_Answer.objects.filter(workshop_id=workshop_id)
                n_ques_answered_total = AkuPoll_Answer.objects.filter(workshop_id=workshop_id).count()
                question_economy = AkuPoll.objects.values_list("economy", flat=True)
                question_care = AkuPoll.objects.values_list("care", flat=True)
                question_technology = AkuPoll.objects.values_list("technology", flat=True)
                question_embedding = AkuPoll.objects.values_list("embedding", flat=True)
                question_law = AkuPoll.objects.values_list("law", flat=True)
                question_ethics = AkuPoll.objects.values_list("ethics", flat=True)
            else: 
                skipped_ques_t = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
                ques_answered_total = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id)
                n_ques_answered_total = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id).count()
                question_economy = AmbuPoll.objects.values_list("economy", flat=True)
                question_care = AmbuPoll.objects.values_list("care", flat=True)
                question_technology = AmbuPoll.objects.values_list("technology", flat=True)
                question_embedding = AmbuPoll.objects.values_list("embedding", flat=True)
                question_law = AmbuPoll.objects.values_list("law", flat=True)
                question_ethics = AmbuPoll.objects.values_list("ethics", flat=True)

            # Get the total number of questions on the table, the answered ones and the remaining ones
            for question_for in question_economy:
                if question_for == "":
                    pass 
                else: 
                    n_ques_total += 1
            
            for question_for in question_care:
                if question_for == "":
                    pass
                else: 
                    n_ques_total += 1
            
            for question_for in question_technology:
                if question_for == "":
                    pass
                else: 
                    n_ques_total += 1
            
            for question_for in question_embedding:
                if question_for == "":
                    pass
                else: 
                    n_ques_total += 1

            for question_for in question_law:
                if question_for == "":
                    pass
                else: 
                    n_ques_total += 1
            
            for question_for in question_ethics:
                if question_for == "":
                    pass
                else: 
                    n_ques_total += 1

            print ("NUM TOTAL QUESTION: ", n_ques_total, flush=True)
            print ("NUM TOTAL ANSWERED: ", n_ques_answered_total, flush=True)

            # 2) If all the questions were answered we need to check if there are skipped questions that have to be shown
            if n_ques_answered_total == n_ques_total:
                print("ALL THE QUESTIONS WERE ANSWERED", flush=True)
                if not skipped_ques_t:
                    return HttpResponseRedirect(reverse('polls:evaluation'))
                else:
                    request.session['skip_id'] = 0
                    return HttpResponseRedirect(reverse('polls:show_skip_ques'))
            #3) If there are still unanswered questions we load the next one
            else: 
                if n_ques_answered_total == 0:
                    category = "care"
                    ques_id = 1
                    return HttpResponseRedirect(reverse('polls:questions', args=(category, ques_id)))
                else:
                    category = ques_answered_total[n_ques_answered_total-1].category
                    ques_id = ques_answered_total[n_ques_answered_total-1].ques_id
                    return HttpResponseRedirect(reverse('polls:next_ques', args=(category, ques_id)))

    elif 'delete_workshop_button' in request.POST: # Delete all the elements related with that workshop
        workshop_id = request.POST.get("workshop_id", "")

        try:
            selected_setting = get_object_or_404(Setting, workshop_id=workshop_id)
            selected_workshop = get_object_or_404(Workshop, workshop_id=workshop_id)
            saved_roles = Roles.objects.filter(workshop_id=workshop_id)
            langpoll_answered_ques = LangPoll_Answer.objects.filter(workshop_id=workshop_id)
            akupoll_answered_ques = AkuPoll_Answer.objects.filter(workshop_id=workshop_id)
            ambupoll_answered_ques = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id)

            selected_setting.delete()
            print ("DELETED SETTING", flush=True)
            saved_roles.delete()
            print("DELETED ROLES")
            langpoll_answered_ques.delete()
            print("DELETED LANGPOLL ANSWERS", flush=True)
            akupoll_answered_ques.delete()
            print("DELETED AKUPOLL ANSWERS", flush=True)
            ambupoll_answered_ques.delete()
            print("DELETED AMBUPOLL ANSWERS", flush=True)
            selected_workshop.delete()
            print("WORKSHOP IS DELETED")

        except:
            selected_workshop = get_object_or_404(Workshop, workshop_id=workshop_id)

            selected_workshop.delete()
            print("WORKSHOP IS DELETED")

        return HttpResponseRedirect(reverse('polls:list_workshop'))

    elif 'back_intro_button' in request.POST: # Delete all the elements related with that workshop
        return render(request, "polls/intro.html")


@login_required(login_url='polls:login_user')
def setting_view(request):
    workshop_id = request.session.get('workshop_id')
    print("WORKSHOP ID: ", workshop_id, flush = True)
    try: # Check if that workshop already has a setting, that means was already started and we want to go back to the introduction slides

        setting = get_object_or_404(Setting, workshop_id=workshop_id)
        roles_saved = Roles.objects.filter(workshop_id=workshop_id)

        # List of roles to show depending on the choosen setting
        if setting.setting == "langzeitstationär":
            selected_Roles = RolesLang.objects.all()
        elif setting.setting == "akutstationär":
            selected_Roles = RolesAku.objects.all()
        else:
            selected_Roles = RolesAmbu.objects.all()
        
        list_selected_Roles = list(selected_Roles)
        list_saved_roles = list(roles_saved)

        for sr in list_saved_roles:
            checked_element = sr
            for role in list_selected_Roles:
                if checked_element.role == role.role_name:
                    list_selected_Roles.remove(role)

        return render(request, "polls/setting_repeat.html", {
            "setting": setting,
            "Roles_Saved": list_saved_roles,
            "Selected_Roles": list_selected_Roles
        })

    except:
        # If it is the first time that the intro is shown then we go to the initial setting page
        # Get all the objects from the roles tables 
        return render(request, "polls/setting.html", {
            "Lang_Roles": RolesLang.objects.all(),
            "Aku_Roles": RolesAku.objects.all(),
            "Ambu_Roles": RolesAmbu.objects.all()
        })



@login_required(login_url='polls:login_user')
def save_setting(request):
    workshop_id = request.session.get('workshop_id')

    try: # Check if that workshop already has a setting
        setting = get_object_or_404(Setting, workshop_id=workshop_id)
        print("SETTING: ", setting.setting, flush=True)

        # 1) Deleate the old roles and save the new ones
        roles_saved = Roles.objects.filter(workshop_id=workshop_id)
        roles_saved.delete()
        print("DELETED ROLES")
        checked_items = request.POST.getlist("teil_role") #Get all the checked boxes by id
        if setting.setting == "langzeitstationär":
            for i in checked_items:
                print (i, flush=True)
                checked_roles = RolesLang.objects.get(role_id=i)
                print ("ROLE NAME: ", checked_roles.role_name, flush=True)
                text_name = request.POST.get(i, "")
                print ("NAMES: ",text_name, flush=True)
                saved_role = Roles(workshop_id=workshop_id, role_id=i, role=checked_roles.role_name, names=text_name)
                saved_role.save()
            # Values to load the last answered question
            skipped_ques_t = LangPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
            ques_answered_total = LangPoll_Answer.objects.filter(workshop_id=workshop_id)
            n_ques_answered_total = LangPoll_Answer.objects.filter(workshop_id=workshop_id).count()
            question_economy = LangPoll.objects.values_list("economy", flat=True)
            question_care = LangPoll.objects.values_list("care", flat=True)
            question_technology = LangPoll.objects.values_list("technology", flat=True)
            question_embedding = LangPoll.objects.values_list("embedding", flat=True)
            question_law = LangPoll.objects.values_list("law", flat=True)
            question_ethics = LangPoll.objects.values_list("ethics", flat=True)

        elif setting.setting == "akutstationär":
            for i in checked_items:
                print (i, flush=True)
                checked_roles = RolesAku.objects.get(role_id=i)
                print ("ROLE NAME: ", checked_roles.role_name, flush=True)
                text_name = request.POST.get(i, "")
                print ("NAMES: ",text_name, flush=True)
                saved_role = Roles(workshop_id=workshop_id, role_id=i, role=checked_roles.role_name, names=text_name)
                saved_role.save()
                print("ROLES SAVED: ", flush=True)
            # Values to load the last answered question
            skipped_ques_t = AkuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
            ques_answered_total = AkuPoll_Answer.objects.filter(workshop_id=workshop_id)
            n_ques_answered_total = AkuPoll_Answer.objects.filter(workshop_id=workshop_id).count()
            question_economy = AkuPoll.objects.values_list("economy", flat=True)
            question_care = AkuPoll.objects.values_list("care", flat=True)
            question_technology = AkuPoll.objects.values_list("technology", flat=True)
            question_embedding = AkuPoll.objects.values_list("embedding", flat=True)
            question_law = AkuPoll.objects.values_list("law", flat=True)
            question_ethics = AkuPoll.objects.values_list("ethics", flat=True)
        else:
            for i in checked_items:
                print (i, flush=True)
                checked_roles = RolesAmbu.objects.get(role_id=i)
                print ("ROLE NAME: ", checked_roles.role_name, flush=True)
                text_name = request.POST.get(i, "")
                print ("NAMES: ",text_name, flush=True)
                saved_role = Roles(workshop_id=workshop_id, role_id=i, role=checked_roles.role_name, names=text_name)
                saved_role.save()
            # Values to load the last answered question
            skipped_ques_t = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
            ques_answered_total = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id)
            n_ques_answered_total = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id).count()
            question_economy = AmbuPoll.objects.values_list("economy", flat=True)
            question_care = AmbuPoll.objects.values_list("care", flat=True)
            question_technology = AmbuPoll.objects.values_list("technology", flat=True)
            question_embedding = AmbuPoll.objects.values_list("embedding", flat=True)
            question_law = AmbuPoll.objects.values_list("law", flat=True)
            question_ethics = AmbuPoll.objects.values_list("ethics", flat=True)

        # Get the total number of questions on the table, the answered ones and the remaining ones
        n_ques_total = 0
        for question_for in question_economy:
            if question_for == "":
                pass 
            else: 
                n_ques_total += 1
        
        for question_for in question_care:
            if question_for == "":
                pass
            else: 
                n_ques_total += 1
        
        for question_for in question_technology:
            if question_for == "":
                pass
            else: 
                n_ques_total += 1
        
        for question_for in question_embedding:
            if question_for == "":
                pass
            else: 
                n_ques_total += 1

        for question_for in question_law:
            if question_for == "":
                pass
            else: 
                n_ques_total += 1
        
        for question_for in question_ethics:
            if question_for == "":
                pass
            else: 
                n_ques_total += 1

        # 2) If all the questions were answered we need to check if there are skipped questions that have to be shown
        if n_ques_answered_total == n_ques_total:
            print("ALL THE QUESTIONS WERE ANSWERED", flush=True)
            if not skipped_ques_t:
                return HttpResponseRedirect(reverse('polls:evaluation'))
            else:
                request.session['skip_id'] = 0
                return HttpResponseRedirect(reverse('polls:show_skip_ques'))
        #3) If there are still unanswered questions we load the next one
        else: 
            if n_ques_answered_total == 0:
                category = "care"
                ques_id = 1
                return HttpResponseRedirect(reverse('polls:questions', args=(category, ques_id)))
            else:
                category = ques_answered_total[n_ques_answered_total-1].category
                ques_id = ques_answered_total[n_ques_answered_total-1].ques_id
                return HttpResponseRedirect(reverse('polls:next_ques', args=(category, ques_id)))
            
    except: #If it is the first time introducing settings we saved everything
        print("SOMETHING FAILED", flush=True)
        #Save company name:
        selected_company = request.POST.get("text_company_name", "")
        # Save setting value to SQL Table:
        selected_setting = request.POST.get("choice_setting", "")
        robot_name = request.POST.get("text_robot_name", "")
        setting_saved = Setting(workshop_id = workshop_id, setting = selected_setting, company_name = selected_company, robot_name=robot_name)
        setting_saved.save()

        setting = get_object_or_404(Setting, workshop_id=workshop_id)
        # Save Role values to SQL Table:
        if setting.setting == "langzeitstationär":
            checked_items = request.POST.getlist("teil_lang") #Get all the checked boxes by id
            for i in checked_items:
                print (i, flush=True)
                checked_roles = RolesLang.objects.get(role_id=i)
                print ("ROLE NAME: ", checked_roles.role_name, flush=True)
                text_name = request.POST.get(i, "")
                print ("NAMES: ",text_name, flush=True)
                saved_role = Roles(workshop_id=workshop_id, role=checked_roles.role_name, names=text_name)
                saved_role.save()
                
        elif setting.setting == "akutstationär":
            checked_items = request.POST.getlist("teil_aku") #Get all the checked boxes 
            for i in checked_items:
                print (i, flush=True)
                checked_roles = RolesAku.objects.get(role_id=i)
                print ("ROLE NAME: ", checked_roles.role_name, flush=True)
                text_name = request.POST.get(i, "")
                print ("NAMES: ",text_name, flush=True)
                saved_role = Roles(workshop_id=workshop_id, role=checked_roles.role_name, names=text_name)
                saved_role.save()
                
        else:
            checked_items = request.POST.getlist("teil_ambu") #Get all the checked boxes 
            for i in checked_items:
                print (i, flush=True)
                checked_roles = RolesAmbu.objects.get(role_id=i)
                print ("ROLE NAME: ", checked_roles.role_name, flush=True)
                text_name = request.POST.get(i, "")
                print ("NAMES: ",text_name, flush=True)
                saved_role = Roles(workshop_id=workshop_id, role=checked_roles.role_name, names=text_name)
                saved_role.save()
                
        
        return HttpResponseRedirect(reverse('polls:questions', args=('care', 1)))


@login_required(login_url='polls:login_user')
def question_view(request, category, question_id): 

    n_ques_total = 0
    workshop_id = request.session.get('workshop_id')
    selected_setting = get_object_or_404(Setting, workshop_id=workshop_id)
    print (selected_setting, flush=True)
    selected_option = ""

    if selected_setting.setting == "langzeitstationär":
        question = get_object_or_404(LangPoll, ques_id=question_id)
        mouse_over = get_object_or_404(LangMouse, ques_id=question_id)
        skipped_ques = LangPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True).count()
        n_ques_answered_total = LangPoll_Answer.objects.filter(workshop_id=workshop_id).count()
        question_economy = LangPoll.objects.values_list("economy", flat=True)
        question_care = LangPoll.objects.values_list("care", flat=True)
        question_technology = LangPoll.objects.values_list("technology", flat=True)
        question_embedding = LangPoll.objects.values_list("embedding", flat=True)
        question_law = LangPoll.objects.values_list("law", flat=True)
        question_ethics = LangPoll.objects.values_list("ethics", flat=True)

    elif selected_setting.setting == "akutstationär":
        question = get_object_or_404(AkuPoll, ques_id=question_id)
        mouse_over = get_object_or_404(AkuMouse, ques_id=question_id)
        skipped_ques = AkuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True).count()
        n_ques_answered_total = AkuPoll_Answer.objects.filter(workshop_id=workshop_id).count()
        question_economy = AkuPoll.objects.values_list("economy", flat=True)
        question_care = AkuPoll.objects.values_list("care", flat=True)
        question_technology = AkuPoll.objects.values_list("technology", flat=True)
        question_embedding = AkuPoll.objects.values_list("embedding", flat=True)
        question_law = AkuPoll.objects.values_list("law", flat=True)
        question_ethics = AkuPoll.objects.values_list("ethics", flat=True)
    else: 
        question = get_object_or_404(AmbuPoll, ques_id=question_id)
        mouse_over = get_object_or_404(AmbuMouse, ques_id=question_id)
        skipped_ques = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True).count()
        n_ques_answered_total = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id).count()
        question_economy = AmbuPoll.objects.values_list("economy", flat=True)
        question_care = AmbuPoll.objects.values_list("care", flat=True)
        question_technology = AmbuPoll.objects.values_list("technology", flat=True)
        question_embedding = AmbuPoll.objects.values_list("embedding", flat=True)
        question_law = AmbuPoll.objects.values_list("law", flat=True)
        question_ethics = AmbuPoll.objects.values_list("ethics", flat=True)

    # Get the total number of questions on the table, the answered ones and the remaining ones
    for question_for in question_economy:
        if question_for == "":
            pass
        else: 
            n_ques_total += 1
    
    for question_for in question_care:
        if question_for == "":
            pass
        else: 
            n_ques_total += 1
    
    for question_for in question_technology:
        if question_for == "":
            pass
        else: 
            n_ques_total += 1
    
    for question_for in question_embedding:
        if question_for == "":
            pass
        else: 
            n_ques_total += 1

    for question_for in question_law:
        if question_for == "":
            pass
        else: 
            n_ques_total += 1
    
    for question_for in question_ethics:
        if question_for == "":
            pass
        else: 
            n_ques_total += 1

    n_ques_answered = n_ques_answered_total - skipped_ques
    n_ques_left = n_ques_total - n_ques_answered

    # Check if the question was previously answered: 
    try: 
        if selected_setting.setting == "langzeitstationär":
            answer_question = get_object_or_404(LangPoll_Answer, workshop_id=workshop_id, category=category, ques_id=question_id)
        elif selected_setting.setting == "akutstationär":
            answer_question = get_object_or_404(AkuPoll_Answer, workshop_id=workshop_id, category=category, ques_id=question_id)
        else: 
            answer_question = get_object_or_404(AmbuPoll_Answer, workshop_id=workshop_id, category=category, ques_id=question_id)

        comment_jaaber = ""
        comment_nein = ""
        comment_unless = ""

        if answer_question.choice == "Ja_aber":
            comment_jaaber = answer_question.comment
        elif answer_question.choice == "nein":
            comment_nein = answer_question.comment
            comment_unless = answer_question.comment_unless
        else:
            print("No need to add comment", flush=True)
        
        return render(request, "polls/question.html", {
            "question": question,
            "next_question" : question_id + 1,
            "question_id" : question_id,
            "comment_jaaber" : comment_jaaber,
            "comment_nein" :  comment_nein,
            "comment_unless" : comment_unless,
            "selected_option" : answer_question.choice,
            "category": category,
            "mouse_over": mouse_over,
            "robot_name": selected_setting.robot_name,
            "n_ques_answered": n_ques_answered,
            "n_ques_left": n_ques_left
        })
    
    except:
        return render(request, "polls/question.html", {
            "question": question,
            "next_question" : question_id + 1,
            "question_id" : question_id,
            "selected_option" : selected_option,
            "category": category,
            "n_ques_answered": n_ques_answered,
            "n_ques_left": n_ques_left,
            "mouse_over": mouse_over,
            "robot_name": selected_setting.robot_name,
        })


@login_required(login_url='polls:login_user')
def next_ques(request, question_id, category): 
    print("INSIDE NEXT_QUES", flush=True)
    workshop_id = request.session.get('workshop_id')
    print("WORKSHOP ID:", workshop_id, flush=True)
    selected_setting = get_object_or_404(Setting, workshop_id=workshop_id)
    print("SETTING: ", selected_setting, flush=True)
    if selected_setting.setting == "langzeitstationär":
        question = get_object_or_404(LangPoll, ques_id=question_id)
        number_rows = LangPoll.objects.count()
        skipped_ques_t = LangPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
    elif selected_setting.setting == "akutstationär":
        question = get_object_or_404(AkuPoll, ques_id=question_id)
        number_rows = AkuPoll.objects.count()
        skipped_ques_t = AkuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
    else: 
        question = get_object_or_404(AmbuPoll, ques_id=question_id)
        number_rows = AmbuPoll.objects.count()
        skipped_ques_t = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)

    print ("NEXT QUESTION CATEGORY IS:", category, flush=True)

    # Increase ID to go to the next question
    next_question = question_id + 1
    # Select the choice(ja, ja aber, nein) submited with the form
    selected_choice = request.POST.get("choice", "")

    try: # If the question was previously filled then we overwrite the data
        if selected_setting.setting == "langzeitstationär":
            answer_question = get_object_or_404(LangPoll_Answer, workshop_id=workshop_id, category=category, ques_id=question_id)
        elif selected_setting.setting == "akutstationär":
            answer_question = get_object_or_404(AkuPoll_Answer, workshop_id=workshop_id, category=category, ques_id=question_id)
        else: 
            answer_question = get_object_or_404(AmbuPoll_Answer, workshop_id=workshop_id, category=category, ques_id=question_id)
        
        if selected_choice == "Ja":
            answer_question.choice = selected_choice
            answer_question.comment = ""
            answer_question.comment_unless = ""
            answer_question.skipped = False
            answer_question.save()
        elif selected_choice == "Ja_aber":
            text_jaaber = request.POST.get("text_jaaber", "")
            answer_question.choice = selected_choice
            answer_question.comment = text_jaaber
            answer_question.comment_unless = ""
            answer_question.skipped = False
            answer_question.save()
        elif selected_choice == "nein":
            text_nein = request.POST.get("text_nein", "")
            text_unless = request.POST.get("text_unless", "")
            answer_question.choice = selected_choice
            answer_question.comment = text_nein
            answer_question.comment_unless = text_unless
            answer_question.skipped = False
            answer_question.save()
        else:
            print ("Empty question", flush=True)

    except: # If the question was not answer we save the values to the database 

        print ("New question", flush=True)
        if selected_setting.setting == "langzeitstationär":
            saved_answer = LangPoll_Answer(question="", choice="", comment="", comment_unless="", ques_id=question_id, category=category, workshop_id=workshop_id)
        elif selected_setting.setting == "akutstationär":
            saved_answer = AkuPoll_Answer(question="", choice="", comment="", comment_unless="", ques_id=question_id, category=category, workshop_id=workshop_id)
        else: 
            saved_answer = AmbuPoll_Answer(question="", choice="", comment="", comment_unless="", ques_id=question_id, category=category, workshop_id=workshop_id)

        if selected_choice == "Ja":
            if category == "economy":
                saved_answer.question = question.economy
            elif category == "care":
                saved_answer.question = question.care
            elif category == "technology":
                saved_answer.question = question.technology
            elif category == "embedding":
                saved_answer.question = question.embedding
            elif category == "law":
                saved_answer.question = question.law
            else:
                saved_answer.question = question.ethics

            saved_answer.choice = selected_choice
            saved_answer.save()
        elif selected_choice == "Ja_aber":
            text_jaaber = request.POST.get("text_jaaber", "")
            if category == "economy":
                saved_answer.question = question.economy
            elif category == "care":
                saved_answer.question = question.care
            elif category == "technology":
                saved_answer.question = question.technology
            elif category == "embedding":
                saved_answer.question = question.embedding
            elif category == "law":
                saved_answer.question = question.law
            else:
                saved_answer.question = question.ethics
            saved_answer.choice = selected_choice
            saved_answer.comment = text_jaaber
            saved_answer.save()
        elif selected_choice == "nein":
            text_nein = request.POST.get("text_nein", "")
            text_unless = request.POST.get("text_unless", "")
            if category == "economy":
                saved_answer.question = question.economy
            elif category == "care":
                saved_answer.question = question.care
            elif category == "technology":
                saved_answer.question = question.technology
            elif category == "embedding":
                saved_answer.question = question.embedding
            elif category == "law":
                saved_answer.question = question.law
            else:
                saved_answer.question = question.ethics
            saved_answer.choice = selected_choice
            saved_answer.comment = text_nein
            saved_answer.comment_unless = text_unless
            saved_answer.save()
        else:
            print ("Empty question", flush=True)

    # If there are still rows in the table we move to the next question of that column
    if next_question <= number_rows:
        if selected_setting.setting == "langzeitstationär":
            question = get_object_or_404(LangPoll, ques_id=next_question)
        elif selected_setting.setting == "akutstationär":
            question = get_object_or_404(AkuPoll, ques_id=next_question)
        else: 
            question = get_object_or_404(AmbuPoll, ques_id=next_question)
            
        # If the question in that row is empty we implement the number and move to the next row
        if (category == "economy" and question.economy == "") or (category == "care" and question.care == "") or (category == "technology" and question.technology == "") or (category == "embedding" and question.embedding == "") or (category == "law" and question.law == "") or (category == "ethics" and question.ethics == ""):
            print ("EMPTY QUESTION", flush=True)
            return HttpResponseRedirect(reverse('polls:next_ques', args=(category, next_question)))
        else:
            print ("GOING TO THE NEXT QUESTION", flush=True)
            return HttpResponseRedirect(reverse('polls:questions', args=(category, next_question))) 
    else: 
        print ("NO MORE ROWS", flush=True)
        if category == "care":
            new_category = "technology"
            next_question = 1
            print ("GOING TO THE NEXT COLUMN", flush=True)
            return HttpResponseRedirect(reverse('polls:questions', args=(new_category, next_question)))
        elif category == "technology":
            new_category = "embedding"
            next_question = 1
            print ("GOING TO THE NEXT COLUMN", flush=True)
            return HttpResponseRedirect(reverse('polls:questions', args=(new_category, next_question)))
        elif category == "embedding":
            new_category = "law"
            next_question = 1
            print ("GOING TO THE NEXT COLUMN", flush=True)
            return HttpResponseRedirect(reverse('polls:questions', args=(new_category, next_question)))
        elif category == "law":
            new_category = "ethics"
            next_question = 1
            print ("GOING TO THE NEXT COLUMN", flush=True)
            return HttpResponseRedirect(reverse('polls:questions', args=(new_category, next_question)))
        elif category == "ethics":
            new_category = "economy"
            next_question = 1
            print ("GOING TO THE NEXT COLUMN", flush=True)
            return HttpResponseRedirect(reverse('polls:questions', args=(new_category, next_question)))
        else:
            print("SKIPPED QUESTIONS: ", skipped_ques_t, flush=True)
            if not skipped_ques_t:
                print("NO SKIPPED QUESTIONS", flush=True)
                return HttpResponseRedirect(reverse('polls:evaluation'))
            else:
                request.session['skip_id'] = 0
                return HttpResponseRedirect(reverse('polls:show_skip_ques'))

@login_required(login_url='polls:login_user')
def prev_ques_lang(request, category, question_id):

    n_ques_total = 0
    comment_jaaber = ""
    comment_nein = ""
    comment_unless = ""

    # First we need to check if the previous question is empty and we have to go another one back
    workshop_id = request.session.get('workshop_id')
    selected_setting = get_object_or_404(Setting, workshop_id=workshop_id)
    if selected_setting.setting == "langzeitstationär":
        number_rows = LangPoll.objects.count()
        skipped_ques = LangPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True).count()
        n_ques_answered_total = LangPoll_Answer.objects.filter(workshop_id=workshop_id).count()
        question_economy = LangPoll.objects.values_list("economy", flat=True)
        question_care = LangPoll.objects.values_list("care", flat=True)
        question_technology = LangPoll.objects.values_list("technology", flat=True)
        question_embedding = LangPoll.objects.values_list("embedding", flat=True)
        question_law = LangPoll.objects.values_list("law", flat=True)
        question_ethics = LangPoll.objects.values_list("ethics", flat=True)
    elif selected_setting.setting == "akutstationär":
        number_rows = AkuPoll.objects.count()
        skipped_ques = AkuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True).count()
        n_ques_answered_total = AkuPoll_Answer.objects.filter(workshop_id=workshop_id).count()
        question_economy = AkuPoll.objects.values_list("economy", flat=True)
        question_care = AkuPoll.objects.values_list("care", flat=True)
        question_technology = AkuPoll.objects.values_list("technology", flat=True)
        question_embedding = AkuPoll.objects.values_list("embedding", flat=True)
        question_law = AkuPoll.objects.values_list("law", flat=True)
        question_ethics = AkuPoll.objects.values_list("ethics", flat=True)
    else: 
        number_rows = AmbuPoll.objects.count()
        skipped_ques = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True).count()
        n_ques_answered_total = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id).count()
        question_economy = AmbuPoll.objects.values_list("economy", flat=True)
        question_care = AmbuPoll.objects.values_list("care", flat=True)
        question_technology = AmbuPoll.objects.values_list("technology", flat=True)
        question_embedding = AmbuPoll.objects.values_list("embedding", flat=True)
        question_law = AmbuPoll.objects.values_list("law", flat=True)
        question_ethics = AmbuPoll.objects.values_list("ethics", flat=True)

    if category == "economy" and question_id == 1:
        prev_question = number_rows
        category = "ethics"
    elif category == "ethics" and question_id == 1:
        prev_question = number_rows
        category = "law"
    elif category == "law" and question_id == 1:
        prev_question = number_rows
        category = "embedding"
    elif category == "embedding" and question_id == 1:
        prev_question = number_rows
        category = "technology"
    elif category == "technology" and question_id == 1:
        prev_question = number_rows
        category = "care"
    elif category == "care" and question_id == 1:
        print ("THERE IS NO PREVIOUS QUESTION", flush=True) 
        return HttpResponseRedirect(reverse('polls:questions', args=(category, question_id,)))
    else: 
        print ("GOING TO THE PREV QUESTION", flush=True)
        prev_question = question_id - 1
    
    #Check if previous question is empty
    if selected_setting.setting == "langzeitstationär":
        question = get_object_or_404(LangPoll, ques_id=prev_question)
        mouse_over = get_object_or_404(LangMouse, ques_id=prev_question)
    elif selected_setting.setting == "akutstationär":
        question = get_object_or_404(AkuPoll, ques_id=prev_question)
        mouse_over = get_object_or_404(AkuMouse, ques_id=prev_question)
    else: 
        question = get_object_or_404(AmbuPoll, ques_id=prev_question)
        mouse_over = get_object_or_404(AmbuMouse, ques_id=prev_question)
    
    if (category == "economy" and question.economy == "") or (category == "care" and question.care == "") or (category == "technology" and question.technology == "") or (category == "embedding" and question.embedding == "") or (category == "law" and question.law == "") or (category == "ethics" and question.ethics == ""):
        print ("EMPTY QUESTION", flush=True)
        return HttpResponseRedirect(reverse('polls:prev_ques_lang', args=(category, prev_question,)))
    else:
        if selected_setting.setting == "langzeitstationär":
            answer_question = get_object_or_404(LangPoll_Answer, workshop_id=workshop_id, category=category, ques_id=prev_question)
        elif selected_setting.setting == "akutstationär":
            answer_question = get_object_or_404(AkuPoll_Answer, workshop_id=workshop_id, category=category, ques_id=prev_question)
        else: 
            answer_question = get_object_or_404(AmbuPoll_Answer, workshop_id=workshop_id, category=category, ques_id=prev_question)

        if answer_question.choice == "Ja_aber":
            comment_jaaber = answer_question.comment
        elif answer_question.choice == "nein":
            comment_nein = answer_question.comment
            comment_unless = answer_question.comment_unless
        else:
            print("No need to add comment", flush=True)
        
        # Get the total number of questions on the table, the answered ones and the remaining ones
        for question_for in question_economy:
            if question_for == "":
                pass
            else: 
                n_ques_total += 1
    
        for question_for in question_care:
            if question_for == "":
                pass
            else: 
                n_ques_total += 1
    
        for question_for in question_technology:
            if question_for == "":
                pass
            else: 
                n_ques_total += 1
    
        for question_for in question_embedding:
            if question_for == "":
                pass
            else: 
                n_ques_total += 1

        for question_for in question_law:
            if question_for == "":
                pass
            else: 
                n_ques_total += 1
    
        for question_for in question_ethics:
            if question_for == "":
                pass
            else: 
                n_ques_total += 1

        n_ques_answered = n_ques_answered_total - skipped_ques
        n_ques_left = n_ques_total - n_ques_answered
        return render(request, "polls/question.html", {
            "question": question,
            "next_question" : prev_question + 1,
            "question_id" : prev_question,
            "comment_jaaber" : comment_jaaber,
            "comment_nein" :  comment_nein,
            "comment_unless" : comment_unless,
            "selected_option" : answer_question.choice,
            "category": category,
            "mouse_over": mouse_over,
            "robot_name": selected_setting.robot_name,
            "n_ques_answered": n_ques_answered,
            "n_ques_left": n_ques_left
        })
            

# Code to skip a question
@login_required(login_url='polls:login_user')
def skip_ques(request, category, question_id):
    print ("QUESTION SKIPPED", flush=True)

    workshop_id = request.session.get('workshop_id')
    selected_setting = get_object_or_404(Setting, workshop_id=workshop_id)
    if selected_setting.setting == "langzeitstationär":
        question = get_object_or_404(LangPoll, ques_id=question_id)
        number_rows = LangPoll.objects.count()
    elif selected_setting.setting == "akutstationär":
        question = get_object_or_404(AkuPoll, ques_id=question_id)
        number_rows = AkuPoll.objects.count()
    else: 
        question = get_object_or_404(AmbuPoll, ques_id=question_id)
        number_rows = AmbuPoll.objects.count()

    next_question = question_id + 1
    selected_choice = request.POST.get("choice", "")
    

    try: # If the question was previously filled then we overwrite the data
        if selected_setting.setting == "langzeitstationär":
            answer_question = get_object_or_404(LangPoll_Answer, workshop_id=workshop_id, category=category, ques_id=question_id)
        elif selected_setting.setting == "akutstationär":
            answer_question = get_object_or_404(AkuPoll_Answer, workshop_id=workshop_id, category=category, ques_id=question_id)
        else: 
            answer_question = get_object_or_404(AmbuPoll_Answer, workshop_id=workshop_id, category=category, ques_id=question_id)
        
        if selected_choice == "Ja_aber":
            text_jaaber = request.POST.get("text_jaaber", "")
            answer_question.comment = text_jaaber
        elif selected_choice == "nein":
            text_nein = request.POST.get("text_nein", "")
            text_unless = request.POST.get("text_unless", "")
            answer_question.comment = text_nein
            answer_question.comment_unless = text_unless

        answer_question.choice = selected_choice
        answer_question.skipped = True
        answer_question.save()

    except: # If the question was not answer we save the values to the database 
        if category == "economy":
            question_value = question.economy
        elif category == "care":
            question_value = question.care
        elif category == "technology":
            question_value = question.technology
        elif category == "embedding":
            question_value = question.embedding
        elif category == "law":
            question_value = question.law
        else:
            question_value = question.ethics

        if selected_setting.setting == "langzeitstationär":
            saved_answer = LangPoll_Answer(question=question_value, choice="selected_choice", comment="", comment_unless="", skipped = True, ques_id=question_id, category=category, workshop_id=workshop_id)
        elif selected_setting.setting == "akutstationär":
            saved_answer = AkuPoll_Answer(question=question_value, choice="selected_choice", comment="", comment_unless="", skipped = True, ques_id=question_id, category=category, workshop_id=workshop_id)
        else: 
            saved_answer = AmbuPoll_Answer(question=question_value, choice="", comment="", comment_unless="", skipped = True, ques_id=question_id, category=category, workshop_id=workshop_id)

        if selected_choice == "Ja_aber":
            text_jaaber = request.POST.get("text_jaaber", "")
            saved_answer.comment = text_jaaber
        elif selected_choice == "nein":
            text_nein = request.POST.get("text_nein", "")
            text_unless = request.POST.get("text_unless", "")
            saved_answer.comment = text_nein
            saved_answer.comment_unless = text_unless

        saved_answer.save()

    # If there are still rows in the table we move to the next question of that column
    if next_question <= number_rows:
        if selected_setting.setting == "langzeitstationär":
            question = get_object_or_404(LangPoll, ques_id=next_question)
        elif selected_setting.setting == "akutstationär":
            question = get_object_or_404(AkuPoll, ques_id=next_question)
        else: 
            question = get_object_or_404(AmbuPoll, ques_id=next_question)
            
        # If the question in that row is empty we implement the number and move to the next row
        if (category == "economy" and question.economy == "") or (category == "care" and question.care == "") or (category == "technology" and question.technology == "") or (category == "embedding" and question.embedding == "") or (category == "law" and question.law == "") or (category == "ethics" and question.ethics == ""):
            print ("EMPTY QUESTION", flush=True)
            return HttpResponseRedirect(reverse('polls:next_ques', args=(category, next_question)))
        else:
            print ("GOING TO THE NEXT QUESTION", flush=True)
            return HttpResponseRedirect(reverse('polls:questions', args=(category, next_question))) 
    else: 
        print ("NO MORE ROWS", flush=True)
        if category == "care":
            new_category = "technology"
            next_question = 1
            print ("GOING TO THE NEXT COLUMN", flush=True)
            return HttpResponseRedirect(reverse('polls:questions', args=(new_category, next_question)))
        elif category == "technology":
            new_category = "embedding"
            next_question = 1
            print ("GOING TO THE NEXT COLUMN", flush=True)
            return HttpResponseRedirect(reverse('polls:questions', args=(new_category, next_question)))
        elif category == "embedding":
            new_category = "law"
            next_question = 1
            print ("GOING TO THE NEXT COLUMN", flush=True)
            return HttpResponseRedirect(reverse('polls:questions', args=(new_category, next_question)))
        elif category == "law":
            new_category = "ethics"
            next_question = 1
            print ("GOING TO THE NEXT COLUMN", flush=True)
            return HttpResponseRedirect(reverse('polls:questions', args=(new_category, next_question)))
        elif category == "ethics":
            new_category = "economy"
            next_question = 1
            print ("GOING TO THE NEXT COLUMN", flush=True)
            return HttpResponseRedirect(reverse('polls:questions', args=(new_category, next_question)))
        else:
            if selected_setting.setting == "langzeitstationär":
                skipped_ques_t = LangPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
            elif selected_setting.setting == "akutstationär":
                skipped_ques_t = AkuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
            else:
                skipped_ques_t = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)

            print("SKIPPED QUESTIONS: ", skipped_ques_t, flush=True)
            if not skipped_ques_t:
                print("NO SKIPPED QUESTIONS", flush=True)
                return HttpResponseRedirect(reverse('polls:evaluation'))
            else:
                new_category = "care"
                request.session['skip_id'] = 0
                return HttpResponseRedirect(reverse('polls:show_skip_ques'))

# Code to show skipped questions
@login_required(login_url='polls:login_user')
def show_skip_ques(request):

    n_ques_total = 0
    workshop_id = request.session.get('workshop_id')
    skip_id = request.session.get('skip_id')
    selected_setting = get_object_or_404(Setting, workshop_id=workshop_id)
    comment_jaaber = ""
    comment_nein = ""
    comment_unless = ""

    # We get all the questions that were skipped for that workshop (aka skipped attribute equals true)
    if selected_setting.setting == "langzeitstationär":
        skipped_ques = LangPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
        mouse_over = get_object_or_404(LangMouse, ques_id=skipped_ques[skip_id].ques_id)
        n_ques_answered_total = LangPoll_Answer.objects.filter(workshop_id=workshop_id).count()
        question_economy = LangPoll.objects.values_list("economy", flat=True)
        question_care = LangPoll.objects.values_list("care", flat=True)
        question_technology = LangPoll.objects.values_list("technology", flat=True)
        question_embedding = LangPoll.objects.values_list("embedding", flat=True)
        question_law = LangPoll.objects.values_list("law", flat=True)
        question_ethics = LangPoll.objects.values_list("ethics", flat=True)
    elif selected_setting.setting == "akutstationär":
        skipped_ques = AkuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
        mouse_over = get_object_or_404(AkuMouse, ques_id=skipped_ques[skip_id].ques_id)
        n_ques_answered_total = AkuPoll_Answer.objects.filter(workshop_id=workshop_id).count()
        question_economy = AkuPoll.objects.values_list("economy", flat=True)
        question_care = AkuPoll.objects.values_list("care", flat=True)
        question_technology = AkuPoll.objects.values_list("technology", flat=True)
        question_embedding = AkuPoll.objects.values_list("embedding", flat=True)
        question_law = AkuPoll.objects.values_list("law", flat=True)
        question_ethics = AkuPoll.objects.values_list("ethics", flat=True)
    else: 
        skipped_ques = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
        mouse_over = get_object_or_404(AmbuMouse, ques_id=skipped_ques[skip_id].ques_id)
        n_ques_answered_total = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id).count()
        question_economy = AmbuPoll.objects.values_list("economy", flat=True)
        question_care = AmbuPoll.objects.values_list("care", flat=True)
        question_technology = AmbuPoll.objects.values_list("technology", flat=True)
        question_embedding = AmbuPoll.objects.values_list("embedding", flat=True)
        question_law = AmbuPoll.objects.values_list("law", flat=True)
        question_ethics = AmbuPoll.objects.values_list("ethics", flat=True)

    # Get the total number of questions on the table, the answered ones and the remaining ones
    for question_for in question_economy:
        if question_for == "":
            print ("EMPTY VALUE")
        else: 
            n_ques_total += 1
    
    for question_for in question_care:
        if question_for == "":
            print ("EMPTY VALUE")
        else: 
            n_ques_total += 1
    
    for question_for in question_technology:
        if question_for == "":
            print ("EMPTY VALUE")
        else: 
            n_ques_total += 1
    
    for question_for in question_embedding:
        if question_for == "":
            print ("EMPTY VALUE")
        else: 
            n_ques_total += 1

    for question_for in question_law:
        if question_for == "":
            print ("EMPTY VALUE")
        else: 
            n_ques_total += 1
    
    for question_for in question_ethics:
        if question_for == "":
            print ("EMPTY VALUE")
        else: 
            n_ques_total += 1

    n_ques_answered = n_ques_answered_total - skipped_ques.count()
    n_ques_left = n_ques_total - n_ques_answered

    # We order in a new list so the skipped questions are shown in the same order as the first time
    final_list_skipped_ques = []
    list_skipped_ques = list(skipped_ques)
    while list_skipped_ques:
        minimum_element = list_skipped_ques[0]
        for question_skip in list_skipped_ques: 
            if question_skip.id < minimum_element.id:
                minimum_element = question_skip
        final_list_skipped_ques.append(minimum_element)
        list_skipped_ques.remove(minimum_element)
    
    # We get the comment for the question, can be empty
    if final_list_skipped_ques[skip_id].choice == "Ja_aber":
        comment_jaaber = final_list_skipped_ques[skip_id].comment
    elif final_list_skipped_ques[skip_id].choice == "nein":
        comment_nein = final_list_skipped_ques[skip_id].comment
        comment_unless = final_list_skipped_ques[skip_id].comment_unless
    else:
        print("No need to add comment", flush=True)

    return render(request, "polls/skipped_question.html", {
        "question": final_list_skipped_ques[skip_id],
        "question_id": final_list_skipped_ques[skip_id].ques_id,
        "comment_jaaber" : comment_jaaber,
        "comment_nein" :  comment_nein,
        "comment_unless" : comment_unless,
        "selected_option" : final_list_skipped_ques[skip_id].choice,
        "category" : final_list_skipped_ques[skip_id].category, 
        "n_ques_answered": n_ques_answered,
        "n_ques_left": n_ques_left,
        "mouse_over": mouse_over 
    })

@login_required(login_url='polls:login_user')
def next_skip_ques(request, category, question_id):

    workshop_id = request.session.get('workshop_id')
    selected_setting = get_object_or_404(Setting, workshop_id=workshop_id)

    # We get all the questions that were skipped (aka skipped=True, because we come from show_skip_ques, we only filter through category and question_id, because the values passed are for skipped_questions only)
    if selected_setting.setting == "langzeitstationär":
        skipped_ques = get_object_or_404(LangPoll_Answer, workshop_id=workshop_id, category=category, ques_id=question_id)
    elif selected_setting.setting == "akutstationär":
        skipped_ques = get_object_or_404(AkuPoll_Answer, workshop_id=workshop_id, category=category, ques_id=question_id)
    else: 
        skipped_ques = get_object_or_404(AmbuPoll_Answer, workshop_id=workshop_id, category=category, ques_id=question_id)

    selected_choice = request.POST.get("choice", "")

    if selected_choice == "Ja":
        skipped_ques.choice = selected_choice
        skipped_ques.skipped = False
        skipped_ques.save()
    elif selected_choice == "Ja_aber":
        text_jaaber = request.POST.get("text_jaaber", "")
        skipped_ques.choice = selected_choice
        skipped_ques.comment = text_jaaber
        skipped_ques.skipped = False
        skipped_ques.save()
    elif selected_choice == "nein":
        text_nein = request.POST.get("text_nein", "")
        text_unless = request.POST.get("text_unless", "")
        skipped_ques.choice = selected_choice
        skipped_ques.comment = text_nein
        skipped_ques.comment_unless = text_unless
        skipped_ques.skipped = False
        skipped_ques.save()
    else:
        print ("Empty question", flush=True)

    if selected_setting.setting == "langzeitstationär":
        skipped_ques_t = LangPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
        n_skipped_ques = skipped_ques_t.count()
    elif selected_setting.setting == "akutstationär":
        skipped_ques_t = AkuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
        n_skipped_ques = AkuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True).count()
    else: 
        skipped_ques_t = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True)
        n_skipped_ques = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True).count()

    # If there are still elements in the skipped questions list then we repeat the process, if not we move on
    if not skipped_ques_t:
        print("NO MORE SKIPPED QUESTIONS", flush=True)
        return HttpResponseRedirect(reverse('polls:evaluation'))
    else:
        skip_id = request.session.get('skip_id')
        if skip_id < n_skipped_ques:
            request.session['skip_id'] = skip_id
            print("GOING TO SHOW SKIP QUES", flush = True)
            
        else:
            request.session['skip_id'] = 0
            print("GOING TO SHOW SKIP QUES WITH SKIP_ID = 0", flush = True)

        return HttpResponseRedirect(reverse('polls:show_skip_ques'))


@login_required(login_url='polls:login_user')
def skip_skip_ques (request):
    workshop_id = request.session.get('workshop_id')
    selected_setting = get_object_or_404(Setting, workshop_id=workshop_id)
    skip_id = request.session.get('skip_id') + 1

    if selected_setting.setting == "langzeitstationär":
        n_skipped_ques = LangPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True).count()
    elif selected_setting.setting == "akutstationär":
        n_skipped_ques = AkuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True).count()
    else: 
        n_skipped_ques = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id, skipped=True).count()
        
    if skip_id < n_skipped_ques:
        request.session['skip_id'] = skip_id
        print("GOING TO SHOW SKIP QUES", flush = True)
        
    else:
        request.session['skip_id'] = 0
        print("GOING TO SHOW SKIP QUES WITH SKIP_ID = 0", flush = True)

    return HttpResponseRedirect(reverse('polls:show_skip_ques'))

@login_required(login_url='polls:login_user')
def evaluation(request):
    return render(request, "polls/evaluation.html")

@login_required(login_url='polls:login_user')
def create_pdf(request):   
    workshop_id = request.session.get('workshop_id')

    # Give name of the workshop to the file
    selected_workshop = get_object_or_404(Workshop, workshop_id=workshop_id)
    filename = selected_workshop.workshop_name + ".pdf"

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    buffer = BytesIO()

    report = MyPrint(buffer, workshop_id)
    pdf = report.print_users()

    response.write(pdf)
    return response

