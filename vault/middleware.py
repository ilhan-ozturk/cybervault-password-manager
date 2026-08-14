class SecurityHeadersMiddleware:
    def __init__(self,get_response): self.get_response=get_response
    def __call__(self,request):
        response=self.get_response(request)
        response['Content-Security-Policy']=("default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'")
        response['Referrer-Policy']='strict-origin-when-cross-origin'
        response['Permissions-Policy']='camera=(), microphone=(), geolocation=(), payment=()'
        response['Cross-Origin-Opener-Policy']='same-origin'
        return response
