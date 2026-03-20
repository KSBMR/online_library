from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

from .views import home, add_book, signupform, user_login, user_logout, bookview, delete_book
# , book_detail


urlpatterns = [
    path('', home, name='home'),
    path('add_book/', add_book, name='add_book'),
    path('signup/', signupform, name='sign_up'),
    path('login/', user_login, name= 'userlogin'),
    path('logout/', user_logout, name= 'userlogout'),
    path('books/<int:pk>/', bookview, name='bookview'),
    path('books/<int:pk>/delete/', delete_book, name='delete_book'),
    # path('book/<int:book_id>/', book_detail, name='book_detail'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
