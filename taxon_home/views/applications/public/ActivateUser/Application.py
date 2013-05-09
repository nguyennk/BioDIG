'''
Application for the Image Editor of the DOME
URL: / or /index.html

Author: Andrew Oberlin
Date: August 5, 2012
'''
from renderEngine.ApplicationBase import ApplicationBase
from django.http import Http404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from taxon_home.views.pagelets.public.NavBarPagelet import NavBarPagelet
from taxon_home.views.pagelets.public.HomePagelet import HomePagelet
from taxon_home.views.pagelets.public.LoginPagelet import LoginPagelet
from taxon_home.views.pagelets.public.FooterPagelet import FooterPagelet

class Application(ApplicationBase):
	def doProcessRender(self,request):
		self.login_value = 0
		try:
			username = request.GET.get('username')
			user = User.objects.get(username=username)
			self.message = 'You have successfully activated your account'
		except User.DoesNotExist:
			raise Http404
		
		user.is_active = True
		user.save()
		
		args={'title':'Activated User'}
		
		self.setApplicationLayout('public/base.html',args)
		self.addPageletBinding('navBar', NavBarPagelet(addHelpButton=True))
		navbarPagelet=NavBarPagelet()
		navbarPagelet.login_links(self.login_value)
		navbarPagelet.login_messages(self.message)
		self.addPageletBinding('navBar',navbarPagelet)
		loginPagelet=LoginPagelet()
		self.addPageletBinding('center-1',loginPagelet)
		self.addPageletBinding('footer',FooterPagelet())
		

		def render(self,request):
			self.doProcessRender(request)
			return self.renderEngine.render(request)
			

'''
Used for mapping to the url in urls.py
'''
def renderAction(request):
	return Application().render(request)
