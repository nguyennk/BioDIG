'''
	ApplicationfortheImageEditoroftheDOME
	URL:/or/index.html
	
	Author:AndrewOberlin
	Date:August5,2012
'''
from renderEngine.ApplicationBase import ApplicationBase
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from taxon_home.views.pagelets.public.NavBarPagelet import NavBarPagelet
from taxon_home.views.pagelets.public.HomePagelet import HomePagelet
from taxon_home.views.pagelets.public.FooterPagelet import FooterPagelet

class Application(ApplicationBase):
	def doProcessRender(self,request):
		self.success=-1
		self.is_register_page=0
		
		if request.method=='POST':
			username=request.POST['username']
			password=request.POST['password']
			email=request.POST['email']
			newuser = User.objects.create_user(username=username,email=email,password=password)
			newuser.save()
			if newuser is not None:
				self.success=1
				user=authenticate(username=username,password=password)
				login(request,user)
			else:
				self.success=0
				
		args = {'Title'	: ''}
		
		self.setApplicationLayout('public/base.html', args)
		self.addPageletBinding('navBar', NavBarPagelet(addHelpButton=True))
		navbarPagelet=NavBarPagelet()
		navbarPagelet.register(self.is_register_page)
		self.addPageletBinding('navBar',navbarPagelet)
		homePagelet=HomePagelet()
		self.addPageletBinding('center-1',homePagelet)
		self.addPageLetBinding('footer',FooterPagelet())
		
	def render(self,request):
		self.doProcessRender(request)
		if self.success==1:
			return HttpResponseRedirect(reverse('taxon_home.views.applications.public.Home.Application.renderAction'))
		else:
			return self.renderEngine.render(request)
	
@csrf_exempt
def renderAction(request):
	return Application().render(request)
