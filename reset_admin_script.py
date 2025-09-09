#!/usr/bin/env python3
"""
Admin User Reset Script
Run this in Render Shell to reset admin credentials
"""

# Copy this code and run in Render Shell:
python_code = '''
from django.contrib.auth.models import User
from django.db import transaction

# Delete existing superusers (optional - if you want fresh start)
print("Current superusers:")
superusers = User.objects.filter(is_superuser=True)
for user in superusers:
    print(f"  - {user.username} ({user.email})")

# Uncomment next lines if you want to delete old admin users
# print("Deleting old superusers...")
# superusers.delete()

# Create new superuser
try:
    with transaction.atomic():
        user = User.objects.create_superuser(
            username='iotadmin',           # Change this
            email='your-email@gmail.com',  # Change this to your email
            password='YourNewPassword123!' # Change this to your password
        )
        print(f"✅ New superuser created: {user.username}")
        print(f"✅ Email: {user.email}")
        print("✅ You can now login to admin panel!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("Try using: python manage.py createsuperuser")
'''

print("📝 COPY AND PASTE THIS INTO RENDER SHELL:")
print("=" * 60)
print("python manage.py shell")
print("")
print("# Then paste this Python code:")
print(python_code)
