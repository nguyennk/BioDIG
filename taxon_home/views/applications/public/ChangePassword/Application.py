'''
	ApplicationfortheImageEditoroftheDOME
	URL:/or/index.html
	
	Author:AndrewOberlin
	Date:August5,2012
'''
from renderEngine.ApplicationBase import ApplicationBase
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from taxon_home.views.pagelets.public.NavBarPagelet import NavBarPagelet
from taxon_home.views.pagelets.public.ChangePasswordPagelet import ChangePasswordPagelet
from taxon_home.views.pagelets.public.LoginPagelet import LoginPagelet
from taxon_home.views.pagelets.public.FooterPagelet import FooterPagelet

class Application(ApplicationBase):
	def doProcessRender(self,request):
		self.success = -1
		self.login_value = 0
		if request.method=='POST':
			username=request.POST['username']
			new_password=request.POST['npassword']
			user = User.objects.get(username=username)
			if user != None:
				user.set_password(new_password)
				user.save()
				self.message = 'Successfully reset password'
				self.login_value = 0
			else:
				self.message = 'The user does not exist'
			
			args = {
				'title'	: 'Login'
				}
		
			self.setApplicationLayout('public/base.html',args)
			self.addPageletBinding('navBar', NavBarPagelet(addHelpButton=True))
			navbarPagelet=NavBarPagelet()
			navbarPagelet.login_links(self.login_value)
			navbarPagelet.login_messages(self.message)
			self.addPageletBinding('navBar',navbarPagelet)
			loginPagelet = LoginPagelet()
			self.addPageletBinding('center-1',loginPagelet)
			self.addPageletBinding('footer',FooterPagelet())
			
		else:
			self.message = 'Reset your password using the form below'
			args = {
				'title'	: 'ChangePassword'
				}
		
			self.setApplicationLayout('public/base.html',args)
			self.addPageletBinding('navBar', NavBarPagelet(addHelpButton=True))
			navbarPagelet=NavBarPagelet()
			navbarPagelet.login_links(self.login_value)
			navbarPagelet.login_messages('')
			self.addPageletBinding('navBar',navbarPagelet)
			changepasswordPagelet = ChangePasswordPagelet()
			changepasswordPagelet.login_messages(self.message)
			self.addPageletBinding('center-1',changepasswordPagelet)
			self.addPageletBinding('footer',FooterPagelet())
		
	def render(self,request):
		self.doProcessRender(request)
		return self.renderEngine.render(request)
	
@csrf_exempt
def renderAction(request):
	return Application().render(request)
