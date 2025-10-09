from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class M1(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info in ['/login/', '/image/code/']:
            return

        info_dict = request.session.get("info")
        if info_dict:
            return
        return redirect('/login/')