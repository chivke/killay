#!/bin/bash
# 
cd /srv/cmpirque
git stash
git pull
sed -i 's/SECRET_DEPLOY = False/SECRET_DEPLOY = True/g' /srv/cmpirque/archivopirke/settings.py
sed -i 's/DEBUG = True/DEBUG = False/g' /srv/cmpirque/archivopirke/settings.py
sed -i 's/DB_DEBUG = True/DB_DEBUG = False/g' /srv/cmpirque/archivopirke/settings.py
sed -i 's/#CSRF_COOKIE_SECURE/CSRF_COOKIE_SECURE/g' /srv/cmpirque/archivopirke/settings.py
sed -i 's/#SESSION_COOKIE_SECURE/SESSION_COOKIE_SECURE/g' /srv/cmpirque/archivopirke/settings.py
sed -i 's/#X_FRAME_OPTIONS/X_FRAME_OPTIONS/g' /srv/cmpirque/archivopirke/settings.py
sed -i 's/#SECURE_CONTENT_TYPE_NOSNIFF/SECURE_CONTENT_TYPE_NOSNIFF/g' /srv/cmpirque/archivopirke/settings.py
sed -i 's/#SECURE_BROWSER_XSS_FILTER/SECURE_BROWSER_XSS_FILTER/g' /srv/cmpirque/archivopirke/settings.py
echo 'Deploy configuration:'
cat /srv/cmpirque/archivopirke/settings.py | grep "SECRET_DEPLOY"
cat /srv/cmpirque/archivopirke/settings.py | grep "^DEBUG"
cat /srv/cmpirque/archivopirke/settings.py | grep "^DB_DEBUG"
cat /srv/cmpirque/archivopirke/settings.py | grep "^CSRF_COOKIE_SECURE"
cat /srv/cmpirque/archivopirke/settings.py | grep "^SESSION_COOKIE_SECURE"
cat /srv/cmpirque/archivopirke/settings.py | grep "^X_FRAME_OPTIONS"
cat /srv/cmpirque/archivopirke/settings.py | grep "^SECURE_CONTENT_TYPE_NOSNIFF"
cat /srv/cmpirque/archivopirke/settings.py | grep "^SECURE_BROWSER_XSS_FILTER"
echo 'updted and secure deployment in settings file.'
