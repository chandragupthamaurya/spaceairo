from django.urls import path
from . import views	
app_name = 'feed'

urlpatterns = [
    path('',views.index,name = 'index'),
    path('create_post/',views.create_post,name = 'create_post'),
    path('editpost/<int:id>/',views.editpost,name='editpost'),
    path('postdetials/<int:id>/',views.postdetails,name='postdetails'),
    path('deletepost/<int:id>/',views.deletepost,name= 'deletepost'),
    path('changeimage/<int:imgid>/<int:postid>/<str:value>/',views.changeimage, name='changeimage'),
	path('like/', views.like, name='post-like'),
	path('deletelike/<int:id>',views.deletelike, name = 'deletelike'),
	path('del_comment/<int:id>/<int:postid>/',views.del_comment,name = 'del_comment'),
	path('categories/<str:value>/',views.categories,name = 'categories'),
	path('wishlist/',views.wishlist,name='wishlist'),
	path('ratingstar/',views.ratingstar,name='ratingstar'),
    ]