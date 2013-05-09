'''
	Application for the Image Editor of the DOME
	URL: / or /index.html
	
	Author: Andrew Oberlin
	Date: August 5, 2012
'''
from renderEngine.ApplicationBase import ApplicationBase
from taxon_home.views.pagelets.public.NavBarPagelet import NavBarPagelet
from taxon_home.views.pagelets.public.HomePagelet import HomePagelet
from taxon_home.views.pagelets.public.FooterPagelet import FooterPagelet

class Application(ApplicationBase):
	def doProcessRender(self, request):
		self.login_value = 1
                self.message = ''
		args = {
			'title' : 'Homepage'
		}
		self.setApplicationLayout('public/base.html', args)
		self.addPageletBinding('navBar', NavBarPagelet(addHelpButton=True))
		navbarPagelet = NavBarPagelet()
                navbarPagelet.login_links(self.login_value)
                navbarPagelet.login_messages(self.message)
		self.addPageletBinding('navBar',navbarPagelet)
		self.addPageletBinding('center-1', HomePagelet())
		self.addPageletBinding('footer', FooterPagelet())
		
'''
	Used for mapping to the url in urls.py
'''        	
def renderAction(request):
	return Application().render(request)

