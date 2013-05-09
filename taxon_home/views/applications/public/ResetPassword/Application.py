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
import uuid
from django.core.mail import EmailMultiAlternatives
from taxon_home.views.pagelets.public.NavBarPagelet import NavBarPagelet
from taxon_home.views.pagelets.public.ResetPasswordPagelet import ResetPasswordPagelet
from taxon_home.views.pagelets.public.FooterPagelet import FooterPagelet

class Application(ApplicationBase):
	def doProcessRender(self,request):
		self.success = -1
		self.login_value = 0
		self.message = ''
		if request.method=='POST':
			user_email=request.POST['email']
			self.message = 'Please check email to reset your password'
			#token = ''.join(random.choice(string.ascii_uppercase + string.digits) for n in range(20))
			token = uuid.uuid4()
			url = 'localhost/changePassword?user=%s' %(token)
			subject, from_email, to = 'Reset Password', 'rajeswari284@gmail.com',user_email
			text_content = ''						
			html_content = '<html><body><p>Please click the link below to reset your password</p><a href=%s>Click Here</a></body></html></p>' %(url)
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			
			args = {
				'title'	: 'Reset'
				}
		
			self.setApplicationLayout('public/base.html',args)
			self.addPageletBinding('navBar', NavBarPagelet(addHelpButton=True))
			navbarPagelet=NavBarPagelet()
			navbarPagelet.login_links(self.login_value)
			navbarPagelet.login_messages('')
			self.addPageletBinding('navBar',navbarPagelet)
			resetpasswordPagelet = ResetPasswordPagelet()
			resetpasswordPagelet.login_messages(self.message)
			self.addPageletBinding('center-1',resetpasswordPagelet)
			self.addPageletBinding('footer',FooterPagelet())
		else:
			args = {
				'title'	: 'Reset'
				}
		
			self.setApplicationLayout('public/base.html',args)
			self.addPageletBinding('navBar', NavBarPagelet(addHelpButton=True))
			navbarPagelet=NavBarPagelet()
			navbarPagelet.login_links(self.login_value)
			navbarPagelet.login_messages('')
			self.addPageletBinding('navBar',navbarPagelet)
			resetpasswordPagelet = ResetPasswordPagelet()
			resetpasswordPagelet.login_messages(self.message)
			self.addPageletBinding('center-1',resetpasswordPagelet)
			self.addPageletBinding('footer',FooterPagelet())	
		
		
	def render(self,request):
		self.doProcessRender(request)
		if self.success == 1:
			return HttpResponseRedirect(reverse('taxon_home.views.applications.public.Home.Application.renderAction'))
		else:
			return self.renderEngine.render(request)
	
@csrf_exempt
def renderAction(request):
	return Application().render(request)
