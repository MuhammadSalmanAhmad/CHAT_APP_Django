
import time

from django.http import HttpResponse

class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # Process the request
        response = self.get_response(request)

        # Calculate the duration
        duration = time.time() - start_time

        # Add a custom header to the response
        response['X-Processing-Time-ms'] = int(duration * 1000)

        # Log the duration
        print(f"Request to {request.path} took {duration:.2f} seconds.")

        return response
    
    def process_exception(self,request,exception):
        print(f"Exception: {exception}")
        return HttpResponse(f"Exception: {exception}")


