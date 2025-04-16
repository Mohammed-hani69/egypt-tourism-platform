from os import environ

# Load from environment variables
STRIPE_SECRET_KEY = environ.get('STRIPE_SECRET_KEY', '')
STRIPE_PUBLIC_KEY = environ.get('STRIPE_PUBLIC_KEY', '')

# Verify keys are valid format
if not STRIPE_SECRET_KEY.startswith('sk_'):
    raise ValueError('Invalid Stripe secret key format. Must start with "sk_"')
    
if not STRIPE_PUBLIC_KEY.startswith('pk_'):
    raise ValueError('Invalid Stripe public key format. Must start with "pk_"')

# Export config
stripe_config = {
    'secret_key': STRIPE_SECRET_KEY,
    'public_key': STRIPE_PUBLIC_KEY
}
