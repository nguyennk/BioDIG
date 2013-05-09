'''
	Pagelet for the Nav Bar on many pages
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from renderEngine.PageletBase import PageletBase
from django.contrib import messages

class NavBarPagelet(PageletBase):
	def __init__(self, addHelpButton=False):
		self.addHelpButton = addHelpButton
	
	'''
		Renders the navigation bar for the website		
	
		Params: request -- the Django request object with the POST & GET args
		
		Returns: Dictionary of arguments for rendering this pagelet
	'''
	def doProcessRender(self, request):
		self.setLayout('public/navBar.html')
		
		if self.login_value == 1:
                        login_param = True
                else:
                        login_param = False

		is_admin_page = False
		
		if (request.method == "GET" and request.GET.has_key('add_login')):                
			is_admin_page = request.GET['add_login']

		if self.message:
                        messages.add_message(request,messages.INFO,self.message)
                else:
                        messages.add_message(request,messages.INFO,'')

                #optionsList = NavBarOption.objects.all().order_by('rank')
                #bannertype_obj = PictureType.objects.get(imageType__exact="banner")
                #banner_img = PictureProp.objects.get(type_id__exact=bannertype_obj.pk).picture_id
                #banner_url = banner_img.imageName

		return {
			'is_admin_page' : is_admin_page,
			'addHelpButton' : self.addHelpButton,
			'login_param'   : login_param
		}
	def login_messages(self,message):
		self.message = message

	def login_links(self,login_value):
		self.login_value = login_value
