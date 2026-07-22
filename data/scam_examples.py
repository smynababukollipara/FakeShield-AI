# ─────────────────────────────────────────────────────────────
# data/scam_examples.py
# A curated set of scam SMS / WhatsApp message examples
# used to test the detector in "SMS mode".
#
# These are fictional examples modelled on real scam patterns —
# they do NOT contain real personal data or phone numbers.
# ─────────────────────────────────────────────────────────────

SCAM_MESSAGES = [
    # Prize / lottery scams
    "Congratulations! You've won a $500 Amazon gift card. "
    "Click here to claim within 24 hours: http://amaz0n-prize.xyz",

    "ALERT: Your account has been selected for a $1,000 bonus reward. "
    "Reply YES to claim. Offer expires tonight!",

    "You are today's lucky winner! Your mobile number won £750,000 "
    "in our international draw. Send name and bank details to claim.",

    # Fake bank / OTP scams
    "URGENT: Your bank account has been suspended due to suspicious activity. "
    "Verify now at http://secure-bank-login.net or lose access permanently.",

    "Your OTP is 847291. NEVER share this with anyone. "
    "If you did not request this, call 0800-FAKE-BANK immediately.",

    # Package delivery scams
    "Your parcel could not be delivered. A fee of £1.99 is outstanding. "
    "Pay here to reschedule delivery: http://royal-mail-redeliver.com",

    "DHL NOTICE: Your package #7823-XQ is on hold. "
    "Confirm your address and pay customs: http://dhl-customs-fee.net",

    # Job / income scams
    "Work from home! Earn $500/day with just 2 hours of work. "
    "No experience needed. WhatsApp us now: +1-555-0199",

    "HIRING: Social media raters needed. $30/hr, flexible hours. "
    "Send your name and email to jobs@easy-earn-online.com to apply.",

    # Government / tax scams
    "HMRC: You are owed a tax refund of £328.50. "
    "Claim it here within 48 hours: http://hmrc-refund-portal.uk",

    "IRS FINAL NOTICE: Failure to call back will result in your arrest. "
    "Call 1-800-TAX-SCAM immediately to resolve your outstanding liability.",
]

REAL_SMS_MESSAGES = [
    # Genuine bank alerts
    "Your HDFC Bank account was debited Rs.1,200 on 08-Jun. "
    "Available balance: Rs.45,320. If not done by you, call 1800-XXX-XXXX.",

    # Genuine delivery notifications
    "Your Amazon order #405-1234567 has been shipped and will arrive by Thursday. "
    "Track your package at amazon.com/orders.",

    # Genuine appointment reminders
    "Reminder: Your dental appointment is tomorrow at 10:30am with Dr. Smith. "
    "Reply CONFIRM to keep or CANCEL to reschedule. No charge for 24hr notice.",

    # Genuine OTP
    "Your verification code for login is 583920. "
    "Valid for 10 minutes. Do not share this code with anyone.",

    # Genuine promotional (opt-in)
    "Hi! Your Starbucks rewards balance is 420 stars. "
    "You're 80 stars away from a free drink. Visit any store to redeem.",
]
