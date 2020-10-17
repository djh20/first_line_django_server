from django.contrib import admin
from .models import Post
from .models import LikeRecord
from .models import LookupRecord
admin.site.register(Post)
admin.site.register(LikeRecord)
admin.site.register(LookupRecord)