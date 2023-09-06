from django.urls import path

from comments.views import CommentListView, CommentDetailsView

app_name = 'comments'
urlpatterns = [
    path('products/<int:pk>/comments', CommentListView.as_view(), name='commnet_list'),
    path('comments/<int:pk>', CommentDetailsView.as_view(), name='comment_details_short'),
    #path('products/<int:pk>/comments/<int:pk>', CommentDetailsView.as_view(),
    #    name='comment_details'),

]
