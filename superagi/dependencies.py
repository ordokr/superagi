# Import the auth functions to make them available as dependencies
from superagi.helper.auth import get_current_user, get_user_organisation, check_auth

# Re-export for backward compatibility
__all__ = ['get_current_user', 'get_user_organisation', 'check_auth']
