def get_user_profile(request):
    if hasattr(request.user, "userprofile"):
        return request.user.userprofile
    return None