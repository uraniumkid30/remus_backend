from conf.addons.directories import (
    STATIC_COLLECTION_DIR,
    MEDIA_DIR,
    STATIC_DIR
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = STATIC_COLLECTION_DIR  # is the folder location of static files when collectstatic is run
MEDIA_URL = "/media/"
MEDIA_ROOT = MEDIA_DIR

STATICFILES_DIRS = [
    STATIC_DIR,
] # tells Django where to look for static files in a Django project, such as a top-level static folder

# DJANGO_STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
# WHITENOISE_STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
