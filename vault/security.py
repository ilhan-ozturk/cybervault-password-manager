import math, re
from datetime import timedelta
from django.utils import timezone

COMMON_PASSWORDS={
    'password','password1','123456','12345678','123456789','qwerty','qwerty123','admin','admin123',
    'letmein','welcome','iloveyou','abc123','111111','000000','monkey','dragon','football','master'
}

def analyze_password(password):
    password=password or ''
    pools=0
    if re.search(r'[a-z]',password): pools+=26
    if re.search(r'[A-Z]',password): pools+=26
    if re.search(r'\d',password): pools+=10
    if re.search(r'[^A-Za-z0-9]',password): pools+=33
    entropy=round(len(password)*math.log2(max(pools,1)),1) if password else 0
    issues=[]
    if len(password)<12: issues.append('Shorter than 12 characters')
    if password.lower() in COMMON_PASSWORDS: issues.append('Found in local common-password list')
    if not re.search(r'[A-Z]',password): issues.append('No uppercase character')
    if not re.search(r'[a-z]',password): issues.append('No lowercase character')
    if not re.search(r'\d',password): issues.append('No number')
    if not re.search(r'[^A-Za-z0-9]',password): issues.append('No symbol')
    if re.search(r'(.){2,}',password): issues.append('Repeated character pattern')
    score=100
    score-=max(0,12-len(password))*5
    if password.lower() in COMMON_PASSWORDS: score-=45
    score-=8*sum(1 for x in ['No uppercase character','No lowercase character','No number','No symbol'] if x in issues)
    if entropy<50: score-=15
    elif entropy<65: score-=5
    score=max(0,min(100,score))
    label='Strong' if score>=80 else 'Good' if score>=60 else 'Weak' if score>=35 else 'Critical'
    return {'score':score,'label':label,'entropy':entropy,'issues':issues}

def is_old(credential, days=180):
    return credential.password_changed_at < timezone.now()-timedelta(days=days)
