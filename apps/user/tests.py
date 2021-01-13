import re
print(re.match(r"/api/rbac/permissions/(?P[^/.]+)/$", '/api/rbac/permissions/1/'))
