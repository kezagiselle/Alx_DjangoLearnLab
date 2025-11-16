"""
Content Security Policy (CSP) Middleware

This middleware adds Content Security Policy headers to all responses
to help prevent Cross-Site Scripting (XSS) attacks.

CSP works by specifying which domains are allowed to load resources
(scripts, styles, images, etc.) in your application.
"""


class ContentSecurityPolicyMiddleware:
    """
    Middleware to add Content Security Policy headers.
    
    CSP helps prevent XSS attacks by controlling which resources
    can be loaded and executed in the browser.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Content Security Policy header
        # This policy allows:
        # - 'self': Resources from the same origin
        # - 'unsafe-inline' for styles: Allows inline styles (can be restricted further)
        # - 'unsafe-inline' for scripts: Allows inline scripts (should be removed in production)
        # 
        # For production, use a stricter policy:
        # "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';"
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        
        response['Content-Security-Policy'] = csp_policy
        
        # X-Content-Type-Options: Prevents MIME type sniffing
        # Already set in settings, but ensuring it's in the response
        response['X-Content-Type-Options'] = 'nosniff'
        
        # X-Frame-Options: Prevents clickjacking
        # Already set in settings, but ensuring it's in the response
        response['X-Frame-Options'] = 'DENY'
        
        # X-XSS-Protection: Enables browser XSS filter
        # Already set in settings, but ensuring it's in the response
        response['X-XSS-Protection'] = '1; mode=block'
        
        return response

