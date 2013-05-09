'''
	Application for the Image Editor of the DOME
	URL: / or /index.html
	
	Author: Andrew Oberlin
	Date: August 5, 2012
'''
from renderEngine.ApplicationBase import ApplicationBase
from taxon_home.views.pagelets.public.NavBarPagelet import NavBarPagelet
from taxon_home.views.pagelets.public.RegisterPagelet import RegisterPagelet
from taxon_home.views.pagelets.public.FooterPagelet import FooterPagelet


class Application(ApplicationBase):
	
	
	def doProcessRender(self, request):
		
		self.is_register_page = 1
	
		args = {
			'title' : 'Register'
		}	
		self.setApplicationLayout('public/base.html', args)
		self.addPageletBinding('navBar', NavBarPagelet(addHelpButton=True))
		navbarpagelet = NavBarPagelet()
		navbarpagelet.register(self.is_register_page)	
		self.addPageletBinding('navBar', navbarpagelet)
		self.addPageletBinding('center-1', RegisterPagelet())
		self.addPageletBinding('footer',FooterPagelet())
'''
	Used for mapping to the url in urls.py
'''	 
#@csrf_exempt	   
def renderAction(request):
	return Application().render(request)
