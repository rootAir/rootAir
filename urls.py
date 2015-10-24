# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_nested import routers

from authentication.views import AccountViewSet, LoginView, LogoutView
from posts.views import AccountPostsViewSet, PostViewSet
# from rootair.views import IndexView

# from finance import views
import hello.views

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'posts', PostViewSet)

accounts_router = routers.NestedSimpleRouter(
    router, r'accounts', lookup='account'
)
accounts_router.register(r'posts', AccountPostsViewSet)

urlpatterns = patterns(
    '',

    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(accounts_router.urls)),
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),

    # url(r'^.*$', IndexView.as_view(), name='index'),
)

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
# admin.autodiscover()

# urlpatterns = patterns('',
#     # Examples:
#     # url(r'^$', 'gettingstarted.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),
#
#     url(r'^$', hello.views.index, name='index'),
#     url(r'^db', hello.views.db, name='db'),
#     url(r'^admin/', include(admin.site.urls)),
# )


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'balance.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # (r'^', include('finance.urls')),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
