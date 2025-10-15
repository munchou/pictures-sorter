@echo off


call "_env/Scripts/activate.bat"

python -m _images_organizer

call deactivate


pause