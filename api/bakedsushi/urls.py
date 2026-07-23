from django.urls import path

from . import views
from . import views_auth
from . import views_store
# from .views import FileUploadView


urlpatterns = [
    # Auth endpoints
    path('auth/google/', views_auth.GoogleLoginView.as_view(), name='auth-google'),
    path('auth/google/callback/', views_auth.GoogleCallbackView.as_view(), name='auth-google-callback'),
    path('auth/me/', views_auth.AuthMeView.as_view(), name='auth-me'),
    path('auth/logout/', views_auth.AuthLogoutView.as_view(), name='auth-logout'),

    # Contact endpoints
    path('contact/list/', views.ContactListView.as_view()),
    path('contact/<int:pk>/', views.ContactDetailView.as_view()),
    path('contact/delete/<int:pk>/', views.ContactCreateView.as_view()),
    path('contact/edit/<int:pk>/', views.ContactCreateView.as_view()),
    path('contact/create/', views.ContactCreateView.as_view()),

    # Products endpoints
    path('products/list/', views_store.ProductListView.as_view()),
    path('products/<int:pk>/', views_store.ProductDetailView.as_view()),

    # Orders endpoints
    path('orders/list/', views_store.OrderListView.as_view()),
    path('orders/<int:pk>/', views_store.OrderDetailView.as_view()),
]