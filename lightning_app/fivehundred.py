"""
Created by @arthurnn on 2012-01-19.
"""

import urllib

# Find a JSON parser
try:
    import json
    _parse_json = lambda s: json.loads(s)
except ImportError:
    try:
        import simplejson
        _parse_json = lambda s: simplejson.loads(s)
    except ImportError:
        # For Google AppEngine
        from django.utils import simplejson
        _parse_json = lambda s: simplejson.loads(s)
        

class FiveHundredPx:
    BASE_URL = 'https://api.500px.com/v1'
    
    def __init__(self,consumer_key):
        self.consumer_key = consumer_key

    def request(self, path, args=None, post_args=None):
        if not args: args = {}
        if self.consumer_key:
            if post_args is not None:
                post_args["consumer_key"] = self.consumer_key
            else:
                args["consumer_key"] = self.consumer_key

        post_data = None if post_args is None else urllib.urlencode(post_args)
        try:
            # HTTP URL used in API
            url = FiveHundredPx.BASE_URL + path + "?" + urllib.urlencode(args, True)
            print url

            file_resp = urllib.urlopen(url, post_data)
            
            data = file_resp.read()
            response = _parse_json(data)
        finally:
            file_resp.close()

        return response

    def get_photos(self, feature='editors', limit=200):
        args = {"feature": feature}
        data = self.request('/photos', args)
        total_pages = data['total_pages']
        page = data['current_page']
        count = 0
        
        while page <= total_pages:
            for p in data['photos']:
                count += 1
                if count > limit: return
                yield p
            
            args['page'] = page = page+1
            data = self.request('/photos', args)
            
    def get_photo(self, id, args = None):
        data = self.request('/photos/%d' % id, args)
        return data
            
    def get_user(self, id=None, username=None, email=None, args = None):
        if id or username or email:
            if id is not None:
                args = {"id": id}
            if username is not None:
                args = {"username": username}
            if email is not None:
                args = {"email": email}

        data = self.request('/users/show', args)
        return data

    def get_user_photos(self, user_id, limit=200):
        args = {
            "feature": "user",
            "user_id": user_id,
            "image_size[]": [1, 2, 3, 4]
        }
        data = self.request('/photos', args)

        total_pages = data['total_pages']
        page = data['current_page']
        count = 0
        
        while page <= total_pages:
            for p in data['photos']:
                count += 1
                if count > limit: return
                yield p
            
            args['page'] = page = page+1
            data = self.request('/photos', args)
