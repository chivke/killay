#!/bin/bash
rm /srv/cmpirque/archivopirke/settings.py
git pull /srv/cmpirque
sed -i 's/SECRET_DEPLOY = False/SECRET_DEPLOY = True/g' /srv/cmpirque/archivopirke/settings.py
sed -i 's/DEBUG = True/DEBUG = False/g' /srv/cmpirque/archivopirke/settings.py
sed -i 's/DB_DEBUG = True/DB_DEBUG = False/g' /srv/cmpirque/archivopirke/settings.py
sed -i 's/#CSRF_COOKIE_SECURE/CSRF_COOKIE_SECURE/g' /srv/cmpirque/archivopirke/settings.py
sed -i 's/#SESSION_COOKIE_SECURE/SESSION_COOKIE_SECURE/g' /srv/cmpirque/archivopirke/settings.py
echo 'updted and secure deployment in settings file.'
