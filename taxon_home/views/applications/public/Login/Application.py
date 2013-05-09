'''
	Application for the Login Handler of the DOME
	URL: /login_handler
	
	Author: Andrew Oberlin
	Date: August 14, 2012
'''
from renderEngine.ApplicationBase import ApplicationBase
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from taxon_home.models import UserProfile
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
import uuid
import sys
from django.core.mail import EmailMultiAlternatives
from taxon_home.views.pagelets.public.NavBarPagelet import NavBarPagelet
from taxon_home.views.pagelets.public.LoginPagelet import LoginPagelet
from taxon_home.views.pagelets.public.FooterPagelet import FooterPagelet

class Application(ApplicationBase):
	def doProcessRender(self, request):
		self.success=-1
                self.login_value = 0
                self.message = 'Welcome to the Login/Registration Page'
                user = None
		newuser = ''

                if request.method=='POST':
                        if not 'email' in request.POST:
                                username=request.POST['username']
                                password=request.POST['password']
                                user=authenticate(username=username,password=password)
                                if user is not None and user.is_active:
                                        login(request,user)
                                        self.message = 'Successfully logged in'
                                        self.success=1
                                else:
                                        self.message = 'Error in login. Please check the values entered'
			elif 'email' in request.POST:
                                username=request.POST['username']
                                password=request.POST['password']
                                email = request.POST['email']
				firstname = request.POST['firstname']
				lastname = request.POST['lastname']
				affiliation = request.POST['affiliation']
                                if authenticate(username=username,password=password) != None:
                                        self.message = 'You already have an account with BioDIG. Log In to get started'
                                else:
					try:
						newuser = User.objects.get(username=username)
						self.message = 'Username already exists. Try a different one.'
						args={'title':'Login'}
                                                self.setApplicationLayout('public/base.html',args)
                                                self.addPageletBinding('navBar', NavBarPagelet(addHelpButton=True))
                                                navbarPagelet=NavBarPagelet()
                                                navbarPagelet.login_links(self.login_value)
                                                navbarPagelet.login_messages(self.message)
                                                self.addPageletBinding('navBar',navbarPagelet)
                                                loginPagelet=LoginPagelet()
                                                self.addPageletBinding('center-1',loginPagelet)
                                                self.addPageletBinding('footer', FooterPagelet())
                                                return HttpResponseRedirect(reverse('taxon_home.views.applications.public.Home.Application.renderAction'))
					except User.DoesNotExist:
						newuser = None
						newuser = User.objects.create_user(username=username,email=email,password=password)
						newuser.is_active = False
						newuser.first_name = firstname
						newuser.last_name = lastname
						newuser.save()
						hex_id = uuid.uuid4()
						hex_user = ''
						for i in str(username):
							hex_user = hex_user + str(ord(i))
						activation_key = str(hex_id) + hex_user
						new_profile = UserProfile(user=newuser, activation_key=activation_key, affiliation=affiliation)
						new_profile.save()
							
							
						self.message = 'Valid credentials.Please check email for activating your account'
						url = 'localhost/activate?username=%s&activationKey=%s' %(str(username),activation_key)
						subject, from_email, to = 'Thank you for registering with BioDIG', 'rajeswari284@gmail.com', email
						text_content = ''
						html_content = '<html><body><p>Please click the link below to activate your account</p><a href=%s>Click Here</a></body></html></p>' %(url)
						msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
						msg.attach_alternative(html_content, "text/html")
						msg.send()
					
                                        
		args={'title':'Login'}

                self.setApplicationLayout('public/base.html',args)
		self.addPageletBinding('navBar', NavBarPagelet(addHelpButton=True))
                navbarPagelet=NavBarPagelet()
                navbarPagelet.login_links(self.login_value)
                navbarPagelet.login_messages(self.message)
                self.addPageletBinding('navBar',navbarPagelet)
                loginPagelet=LoginPagelet()
                self.addPageletBinding('center-1',loginPagelet)
		self.addPageletBinding('footer', FooterPagelet())
		#if (request.method == "POST"):
		#	username = request.POST['username']
		#	password = request.POST['password']
		#	user = authenticate(username=username, password=password)
		#	if user is not None and user.is_active:
		#		login(request, user)

	def render(self, request):
		self.doProcessRender(request)
                if self.success==1:
                        return HttpResponseRedirect(reverse('taxon_home.views.applications.public.Home.Application.renderAction'))
                else:
                        return self.renderEngine.render(request)
		#self.doProcessRender(request)
		#return HttpResponseRedirect(
		#	reverse('taxon_home.views.applications.public.Home.Application.renderAction')
		#)


'''
	Used for mapping to the url in urls.py
'''  
@csrf_exempt      	
def renderAction(request):
	return Application().render(request)

