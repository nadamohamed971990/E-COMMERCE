from django.urls import path
from base.views import user_views as views


urlpatterns = [
    # path('password_reset/<str:pk>', views.CustomPasswordResetView.as_view(), name='reset-password'),
    path('register/',views.registerUser,name='register'),
    path('',views.getUsers,name="users"),
    path('profile/',views.getUserProfile,name="user_profile"),
    path('upload/',views.uploadImage,name="upload_image"),
    path('profile/update/',views.updateUserProfile,name="user_profile_update"),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('<str:pk>/',views.getUserById,name="get_user"),
    path('update/<str:pk>/',views.updateUser,name="updateUser"),
    path('delete/<str:pk>/',views.deleteUser,name="deleteUser"),
]

    # path('password_reset/', views.CustomPasswordResetView.as_view(), name='reset-password'),
    # path('reset-password-confirm/', views.CustomPasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    # path('<int:pk>/', views.UserDetailView.as_view(), name='user-detail')
    # path("password_reset/<str:pk>/", views.ChangePasswordView.as_view(), name="password_reset"),
    # path("reset_password_confirm/", views.passwordResetConfirm, name="reset_password_confirm"),


    # path("password_reset/", views.passwordResetRequest, name="password_reset"),