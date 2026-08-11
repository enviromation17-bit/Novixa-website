[1mdiff --git a/backend/.env b/backend/.env[m
[1mindex fcdf155..186e4c0 100644[m
[1m--- a/backend/.env[m
[1m+++ b/backend/.env[m
[36m@@ -3,5 +3,5 @@[m [mALGORITHM=HS256[m
 ACCESS_TOKEN_EXPIRE_MINUTES=60[m
 [m
 ADMIN_USERNAME=admin[m
[31m-ADMIN_PASSWORD_HASH=$argon2id$v=19$m=65536,t=3,p=4$lOKjkmTSzN9E81ulB4VkAA$RQiMP2SfSU4hRtOIxE4ToH4sYT6G0v54fcz024zs27I[m
[32m+[m[32mADMIN_PASSWORD_HASH=$argon2id$v=19$m=65536,t=3,p=4$eRibBWcLZ9X6LWvvg26NEw$aPc0FsaxYW0Bd85x+lx6Q3amHx6iH09NVa1QBSLpV74[m
 DATABASE_URL=sqlite:///novixa.db[m
\ No newline at end of file[m
[1mdiff --git a/backend/app/core/__pycache__/config.cpython-314.pyc b/backend/app/core/__pycache__/config.cpython-314.pyc[m
[1mindex b0a7573..b0e2d8a 100644[m
Binary files a/backend/app/core/__pycache__/config.cpython-314.pyc and b/backend/app/core/__pycache__/config.cpython-314.pyc differ
[1mdiff --git a/backend/app/core/__pycache__/security.cpython-314.pyc b/backend/app/core/__pycache__/security.cpython-314.pyc[m
[1mindex 369ce41..cc61aaa 100644[m
Binary files a/backend/app/core/__pycache__/security.cpython-314.pyc and b/backend/app/core/__pycache__/security.cpython-314.pyc differ
[1mdiff --git a/backend/app/core/config.py b/backend/app/core/config.py[m
[1mindex bf0a608..84d9b6a 100644[m
[1m--- a/backend/app/core/config.py[m
[1m+++ b/backend/app/core/config.py[m
[36m@@ -5,11 +5,8 @@[m [mload_dotenv()[m
 [m
 [m
 class Settings:[m
[31m-[m
     def __init__(self):[m
[31m-[m
         self.SECRET_KEY = os.getenv("SECRET_KEY")[m
[31m-[m
         self.ALGORITHM = os.getenv("ALGORITHM", "HS256")[m
 [m
         self.ACCESS_TOKEN_EXPIRE_MINUTES = int([m
[36m@@ -17,11 +14,12 @@[m [mclass Settings:[m
         )[m
 [m
         self.ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")[m
[31m-[m
         self.ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")[m
[32m+[m
         self.DATABASE_URL = os.getenv([m
[31m-    "DATABASE_URL",[m
[31m-    "sqlite:///novixa.db"[m
[31m-)[m
[32m+[m[32m            "DATABASE_URL",[m
[32m+[m[32m            "sqlite:///novixa.db",[m
[32m+[m[32m        )[m
[32m+[m
 [m
 settings = Settings()[m
\ No newline at end of file[m
[1mdiff --git a/backend/app/core/security.py b/backend/app/core/security.py[m
[1mindex 24bbf68..a9a9408 100644[m
[1m--- a/backend/app/core/security.py[m
[1m+++ b/backend/app/core/security.py[m
[36m@@ -1,32 +1,32 @@[m
[31m-from datetime import datetime, timedelta[m
[32m+[m[32mfrom datetime import datetime, timedelta, timezone[m
 [m
 from jose import jwt[m
 from pwdlib import PasswordHash[m
[32m+[m
 from app.core.config import settings[m
[32m+[m
 password_hash = PasswordHash.recommended()[m
 [m
[31m-def hash_password(password: str):[m
[32m+[m
[32m+[m[32mdef hash_password(password: str) -> str:[m
     return password_hash.hash(password)[m
 [m
 [m
[31m-def verify_password(password: str, hashed: str):[m
[32m+[m[32mdef verify_password(password: str, hashed: str) -> bool:[m
     return password_hash.verify(password, hashed)[m
 [m
 [m
[31m-def create_access_token(data: dict):[m
[31m-[m
[32m+[m[32mdef create_access_token(data: dict) -> str:[m
     to_encode = data.copy()[m
[32m+[m[41m    [m
[32m+[m[32m    expire = datetime.now(timezone.utc) + timedelta([m
[32m+[m[32m    minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES[m
[32m+[m[32m)[m
 [m
[31m-    expire = datetime.utcnow() + timedelta([m
[31m-        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES[m
[31m-    )[m
[31m-[m
[31m-    to_encode.update([m
[31m-        {"exp": expire}[m
[31m-    )[m
[32m+[m[32m    to_encode.update({"exp": expire})[m
 [m
     return jwt.encode([m
         to_encode,[m
         settings.SECRET_KEY,[m
[31m-        algorithm=settings.ALGORITHM[m
[32m+[m[32m        algorithm=settings.ALGORITHM,[m
     )[m
\ No newline at end of file[m
[1mdiff --git a/backend/app/models/__pycache__/contact.cpython-314.pyc b/backend/app/models/__pycache__/contact.cpython-314.pyc[m
[1mindex 44747d3..2a11115 100644[m
Binary files a/backend/app/models/__pycache__/contact.cpython-314.pyc and b/backend/app/models/__pycache__/contact.cpython-314.pyc differ
[1mdiff --git a/backend/app/models/contact.py b/backend/app/models/contact.py[m
[1mindex 262bc87..da0d3fb 100644[m
[1m--- a/backend/app/models/contact.py[m
[1m+++ b/backend/app/models/contact.py[m
[36m@@ -1,5 +1,6 @@[m
[31m-from sqlalchemy import Column, Integer, String[m
[32m+[m[32mfrom datetime import datetime[m
 [m
[32m+[m[32mfrom sqlalchemy import Column, Integer, String, DateTime[m
 from app.database import Base[m
 [m
 [m
[36m@@ -16,4 +17,17 @@[m [mclass Contact(Base):[m
 [m
     project = Column(String)[m
 [m
[31m-    message = Column(String, nullable=False)[m
\ No newline at end of file[m
[32m+[m[32m    message = Column(String, nullable=False)[m
[32m+[m
[32m+[m[32m    status = Column([m
[32m+[m[32m        String,[m
[32m+[m[32m        nullable=False,[m
[32m+[m[32m        default="new",[m
[32m+[m[32m        index=True,[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    created_at = Column([m
[32m+[m[32m        DateTime,[m
[32m+[m[32m        nullable=False,[m
[32m+[m[32m        default=datetime.utcnow,[m
[32m+[m[32m    )[m
\ No newline at end of file[m
[1mdiff --git a/backend/app/routes/v1/__pycache__/auth.cpython-314.pyc b/backend/app/routes/v1/__pycache__/auth.cpython-314.pyc[m
[1mindex c662359..5690a7b 100644[m
Binary files a/backend/app/routes/v1/__pycache__/auth.cpython-314.pyc and b/backend/app/routes/v1/__pycache__/auth.cpython-314.pyc differ
[1mdiff --git a/backend/app/routes/v1/__pycache__/contact.cpython-314.pyc b/backend/app/routes/v1/__pycache__/contact.cpython-314.pyc[m
[1mindex 0a8a15b..8bdee65 100644[m
Binary files a/backend/app/routes/v1/__pycache__/contact.cpython-314.pyc and b/backend/app/routes/v1/__pycache__/contact.cpython-314.pyc differ
[1mdiff --git a/backend/app/routes/v1/auth.py b/backend/app/routes/v1/auth.py[m
[1mindex db9fad7..b011734 100644[m
[1m--- a/backend/app/routes/v1/auth.py[m
[1m+++ b/backend/app/routes/v1/auth.py[m
[36m@@ -1,3 +1,4 @@[m
[32m+[m[32mprint("AUTH.PY LOADED")[m
 from fastapi import APIRouter, HTTPException[m
 [m
 from app.schemas.auth import LoginRequest [m
[36m@@ -16,27 +17,17 @@[m [mrouter = APIRouter()[m
 )[m
 def login(data: LoginRequest):[m
 [m
[31m-    if ([m
[31m-        data.username == settings.ADMIN_USERNAME[m
[31m-        and verify_password([m
[32m+[m[32m    print("ENV USER:", settings.ADMIN_USERNAME)[m
[32m+[m[32m    print("INPUT USER:", data.username)[m
[32m+[m[32m    print("HASH:", settings.ADMIN_PASSWORD_HASH)[m
[32m+[m
[32m+[m[32m    print([m
[32m+[m[32m        "PASSWORD MATCH:",[m
[32m+[m[32m        verify_password([m
             data.password,[m
[31m-            settings.   ADMIN_PASSWORD_HASH[m
[31m-        )[m
[31m-    ):[m
[31m-        access_token = create_access_token([m
[31m-            {"sub": data.username}[m
[32m+[m[32m            settings.ADMIN_PASSWORD_HASH[m
         )[m
[31m-        return {[m
[31m-            "access_token": access_token,[m
[31m-            "token_type": "bearer"[m
[31m-        }[m
[31m-    [m
[31m-    raise HTTPException([m
[31m-        status_code=401,[m
[31m-        detail="Invalid Username or Password"[m
     )[m
[31m-    [m
[31m-def login(data: LoginRequest):[m
 [m
     if ([m
         data.username == settings.ADMIN_USERNAME[m
[36m@@ -48,7 +39,6 @@[m [mdef login(data: LoginRequest):[m
         access_token = create_access_token([m
             {"sub": data.username}[m
         )[m
[31m-[m
         return {[m
             "access_token": access_token,[m
             "token_type": "bearer"[m
[1mdiff --git a/backend/app/routes/v1/contact.py b/backend/app/routes/v1/contact.py[m
[1mindex 4fcede4..7ff57a1 100644[m
[1m--- a/backend/app/routes/v1/contact.py[m
[1m+++ b/backend/app/routes/v1/contact.py[m
[36m@@ -75,7 +75,8 @@[m [mdef submit_contact([m
             company=data.company,[m
             email=data.email,[m
             project=data.project,[m
[31m-            message=data.message[m
[32m+[m[32m            message=data.message,[m
[32m+[m[32m            status="new"[m
         )[m
         db.add(new_contact)[m
         db.commit()[m
[1mdiff --git a/backend/app/services/contact_service.py b/backend/app/services/contact_service.py[m
[1mindex 0ccd1b6..a57060d 100644[m
[1m--- a/backend/app/services/contact_service.py[m
[1m+++ b/backend/app/services/contact_service.py[m
[36m@@ -15,7 +15,8 @@[m [mdef create_contact([m
         company=data.company,[m
         email=data.email,[m
         project=data.project,[m
[31m-        message=data.message[m
[32m+[m[32m        message=data.message,[m
[32m+[m[32m        status="new",[m
     )[m
 [m
     new_contact = save_contact([m
[1mdiff --git a/backend/logs/novixa.log b/backend/logs/novixa.log[m
[1mindex 0f6a022..16fc1b1 100644[m
[1m--- a/backend/logs/novixa.log[m
[1m+++ b/backend/logs/novixa.log[m
[36m@@ -550,3 +550,59 @@[m [mTypeError: hash must be str or bytes[m
 2026-08-07 16:20:20,755 | INFO | [fb3f4956-2a53-412b-82f6-ee399573397d] GET /health 200 0.0151s[m
 2026-08-07 16:20:52,885 | INFO | [ec57921e-072f-4286-b7c5-621207b0e530] GET /health 200 0.0131s[m
 2026-08-07 16:23:16,318 | INFO | [9b1bfe05-2c62-4ba2-be39-edfee2bba49d] POST /api/v1/login 401 0.0245s[m
[32m+[m[32m2026-08-07 16:58:48,256 | INFO | [66ac79bf-63f0-4d53-9e6e-6172bc9e2e6c] GET /api/v1/contacts 401 0.0128s[m
[32m+[m[32m2026-08-07 17:03:11,639 | INFO | [a654052a-260b-4bf8-a1f5-55e1770a60f8] GET /api/v1/contacts 401 0.0185s[m
[32m+[m[32m2026-08-07 17:13:24,069 | INFO | [a90b712a-0457-4ede-a15b-60d87a391022] POST /api/v1/login 401 0.0142s[m
[32m+[m[32m2026-08-07 17:13:24,337 | INFO | [cadc2cb6-f47e-4f9d-ab00-1df230b49bc4] POST /api/v1/login 401 0.2415s[m
[32m+[m[32m2026-08-07 17:13:42,939 | INFO | [21bb2d22-2806-45ca-9caf-563a77d6d550] POST /api/v1/login 401 0.0292s[m
[32m+[m[32m2026-08-07 17:13:43,348 | INFO | [1ff1b31b-3e3f-4b18-80cd-e3bc7bf4a7af] POST /api/v1/login 401 0.3352s[m
[32m+[m[32m2026-08-07 17:20:45,794 | INFO | [bfa0552c-e585-457f-a79b-5a73ed786547] POST /api/v1/login 401 0.0181s[m
[32m+[m[32m2026-08-07 17:20:46,059 | INFO | [d517f469-1473-46d6-8dd1-8044d9ed54d4] POST /api/v1/login 401 0.2521s[m
[32m+[m[32m2026-08-07 17:34:21,753 | INFO | [ea0bc51a-77aa-464b-8af5-ceebdacd1d0b] POST /api/v1/login 401 0.0221s[m
[32m+[m[32m2026-08-07 17:34:22,040 | INFO | [32d110bb-e120-4330-a206-750466887675] POST /api/v1/login 401 0.2569s[m
[32m+[m[32m2026-08-07 17:36:51,569 | INFO | [61189ade-8550-4894-8e17-09a4ab623709] POST /api/v1/login 401 0.0208s[m
[32m+[m[32m2026-08-07 17:36:51,827 | INFO | [7b6098e4-2148-4611-83da-3193e6ac6417] POST /api/v1/login 401 0.2421s[m
[32m+[m[32m2026-08-07 17:54:58,787 | INFO | [33ae1c77-31b9-46f7-8b83-4de94734308b] POST /api/v1/login 401 0.2533s[m
[32m+[m[32m2026-08-07 17:54:59,312 | INFO | [b7c627b0-9fc7-4ad4-a962-6d03048bbbab] POST /api/v1/login 401 0.5135s[m
[32m+[m[32m2026-08-07 18:01:27,541 | INFO | [7f60ff61-48e2-45fb-8598-1d96cc190f1b] POST /api/v1/login 401 0.2682s[m
[32m+[m[32m2026-08-07 18:01:28,040 | INFO | [76028bfb-03b1-40a8-adfb-71ffe7c6f306] POST /api/v1/login 401 0.4831s[m
[32m+[m[32m2026-08-07 19:01:31,555 | INFO | [df739b70-9b83-4a88-8193-36e69ee07b53] POST /api/v1/login 401 0.2776s[m
[32m+[m[32m2026-08-07 19:01:32,045 | INFO | [0ccf3a81-6711-4619-a723-341fae304cd3] POST /api/v1/login 401 0.4778s[m
[32m+[m[32m2026-08-08 09:01:28,782 | INFO | [fc896a74-c8b3-496b-8ac3-2481268fe00f] POST /api/v1/login 401 0.4685s[m
[32m+[m[32m2026-08-08 09:01:29,416 | INFO | [a58dd142-7334-472a-a995-a0e6aa1eff98] POST /api/v1/login 200 0.5797s[m
[32m+[m[32m2026-08-08 09:09:55,102 | INFO | [fda4ddb2-79eb-43c5-b863-5afec75da625] POST /api/v1/login 401 0.2772s[m
[32m+[m[32m2026-08-08 09:09:55,599 | INFO | [a6ac9aea-0694-4342-8395-0e76ea51c855] POST /api/v1/login 200 0.4817s[m
[32m+[m[32m2026-08-08 09:09:55,616 | INFO | [f3c959f3-be69-40a9-9637-e7857dded4fa] GET /api/v1/contacts 401 0.0058s[m
[32m+[m[32m2026-08-08 09:09:55,641 | INFO | [5a6c4866-ade6-4815-b61c-b77e87e9819a] GET /health 200 0.0064s[m
[32m+[m[32m2026-08-08 09:17:43,477 | INFO | [09edab40-dc4e-4c4c-88e5-1863917ecba6] GET /api/v1/contacts 401 0.0122s[m
[32m+[m[32m2026-08-08 09:25:16,395 | INFO | [e33226ad-d008-49ed-b005-ef19b5c714e5] GET /api/v1/contacts 401 0.0109s[m
[32m+[m[32m2026-08-08 09:25:16,901 | INFO | [c253267e-4801-4c4e-9efb-303346be8322] POST /api/v1/login 200 0.4863s[m
[32m+[m[32m2026-08-08 09:25:16,942 | INFO | [d5985eb2-827f-4311-8058-a99f8b19fb02] GET /api/v1/contacts 200 0.0346s[m
[32m+[m[32m2026-08-08 09:32:28,982 | INFO | [60bc384c-6625-40a1-9411-11149fbf00de] POST /api/v1/login 401 0.2680s[m
[32m+[m[32m2026-08-08 09:32:29,489 | INFO | [26f588ae-fa65-4821-8bb9-9398d8bb65e2] POST /api/v1/login 200 0.4956s[m
[32m+[m[32m2026-08-08 09:32:29,505 | INFO | [cf760200-9607-4711-b583-02d82a8c455d] GET /api/v1/contacts 401 0.0059s[m
[32m+[m[32m2026-08-08 09:32:30,093 | INFO | [f7ca2639-c1be-435f-81c1-1d9117c30e36] POST /api/v1/login 200 0.5735s[m
[32m+[m[32m2026-08-08 09:32:30,125 | INFO | [82578fad-c60a-4132-8a10-5da6c8e73deb] GET /api/v1/contacts 200 0.0251s[m
[32m+[m[32m2026-08-08 09:32:30,181 | INFO | [393ee141-bacc-4e9c-aaf3-1fc8fca05d74] GET /health 200 0.0336s[m
[32m+[m[32m2026-08-08 09:56:40,218 | INFO | [af2415fc-a27c-4905-a5bd-8ae0b91dc0b4] GET /api/v1/services 200 0.0098s[m
[32m+[m[32m2026-08-08 09:57:14,008 | INFO | [42ebcce1-47d7-4f69-af82-88b89138dafe] POST /api/v1/login 401 0.2851s[m
[32m+[m[32m2026-08-08 09:57:14,489 | INFO | [e0ea8de4-41f2-41e8-a9bf-30038cfd14bf] POST /api/v1/login 200 0.4687s[m
[32m+[m[32m2026-08-08 09:57:14,504 | INFO | [cba7ea78-2ea7-4c3e-959b-ca2eaaf31633] GET /api/v1/contacts 401 0.0050s[m
[32m+[m[32m2026-08-08 09:57:15,000 | INFO | [c156f917-9f68-45ae-be79-4632bdea6991] POST /api/v1/login 200 0.4850s[m
[32m+[m[32m2026-08-08 09:57:15,028 | INFO | [6c4f9134-f969-45c1-9fb1-6d833e3bb1ae] GET /api/v1/contacts 200 0.0213s[m
[32m+[m[32m2026-08-08 09:57:15,041 | INFO | [9d8a8dfa-13a3-4a38-b16d-3256304d5bdf] GET /health 200 0.0033s[m
[32m+[m[32m2026-08-08 09:57:15,058 | INFO | [19041ec6-bdd0-4dea-bfc3-c42be3bb7386] GET /api/v1/services 200 0.0056s[m
[32m+[m[32m2026-08-08 10:17:11,459 | INFO | [3aea7646-1cac-48eb-82f4-4bbad65a2122] GET /api/v1/contacts 401 0.0119s[m
[32m+[m[32m2026-08-08 10:17:11,982 | INFO | [b3ca8c31-3832-4134-ba1c-a35dd0917b48] POST /api/v1/login 200 0.5085s[m
[32m+[m[32m2026-08-08 10:17:12,019 | INFO | [ef8dc464-e717-4584-bbf8-b5087c85aaa2] GET /api/v1/contacts 200 0.0306s[m
[32m+[m[32m2026-08-08 10:17:12,066 | INFO | New contact received from Salman Bari (salman@novixa.com)[m
[32m+[m[32m2026-08-08 10:17:12,071 | INFO | [7e05d9ab-72db-4965-8118-1ceb467da46e] POST /api/v1/contacts 200 0.0409s[m
[32m+[m[32m2026-08-09 11:05:14,152 | INFO | [da0c9b67-0136-4c67-ab1a-0d88c7fcf5e0] POST /api/v1/login 401 0.3630s[m
[32m+[m[32m2026-08-09 11:05:14,767 | INFO | [b208e4f3-642f-4b5d-bc9b-bcdb23259141] POST /api/v1/login 200 0.5989s[m
[32m+[m[32m2026-08-09 11:05:14,780 | INFO | [f74e52fc-8cbd-488b-b2c9-b6d3a7368681] GET /api/v1/contacts 401 0.0038s[m
[32m+[m[32m2026-08-09 11:05:15,260 | INFO | [ce1204b5-a152-4703-9f12-7eee9877fbde] POST /api/v1/login 200 0.4647s[m
[32m+[m[32m2026-08-09 11:05:15,281 | INFO | [b68869c2-18d0-4103-8af1-978e6da9abee] GET /api/v1/contacts 200 0.0161s[m
[32m+[m[32m2026-08-09 11:05:15,324 | INFO | New contact received from Salman Bari (salman@novixa.com)[m
[32m+[m[32m2026-08-09 11:05:15,328 | INFO | [9db93fd3-6495-4c97-a8c2-adbad53318b6] POST /api/v1/contacts 200 0.0365s[m
[32m+[m[32m2026-08-09 11:05:15,349 | INFO | [b938ed04-c32c-4c82-b276-c1d5e314dc3d] GET /health 200 0.0049s[m
[32m+[m[32m2026-08-09 11:05:15,371 | INFO | [a2a0df88-871c-42ed-9479-e8a57383284f] GET /api/v1/services 200 0.0090s[m
[1mdiff --git a/backend/novixa.db b/backend/novixa.db[m
[1mindex abe47e5..0cff01c 100644[m
Binary files a/backend/novixa.db and b/backend/novixa.db differ
[1mdiff --git a/backend/tests/__pycache__/test_auth.cpython-314-pytest-9.1.1.pyc b/backend/tests/__pycache__/test_auth.cpython-314-pytest-9.1.1.pyc[m
[1mindex 9fb4a92..7372d1e 100644[m
Binary files a/backend/tests/__pycache__/test_auth.cpython-314-pytest-9.1.1.pyc and b/backend/tests/__pycache__/test_auth.cpython-314-pytest-9.1.1.pyc differ
[1mdiff --git a/backend/tests/test_auth.py b/backend/tests/test_auth.py[m
[1mindex 4d6ddbc..088ef56 100644[m
[1m--- a/backend/tests/test_auth.py[m
[1m+++ b/backend/tests/test_auth.py[m
[36m@@ -22,9 +22,10 @@[m [mdef test_login_success():[m
         "/api/v1/login",[m
         json={[m
             "username": "admin",[m
[31m-            "password": "$argon2id$v=19$m=65536,t=3,p=4$lOKjkmTSzN9E81ulB4VkAA$RQiMP2SfSU4hRtOIxE4ToH4sYT6G0v54fcz024zs27I"[m
[32m+[m[32m            "password": "admin123"[m
         }[m
     )[m
[32m+[m[41m        [m
 [m
     assert response.status_code == 200[m
 [m
[36m@@ -33,4 +34,21 @@[m [mdef test_login_success():[m
     assert "access_token" in data[m
 [m
     assert data["token_type"] == "bearer"[m
[32m+[m[41m    [m
[32m+[m[32mfrom fastapi.testclient import TestClient[m
[32m+[m[32mfrom app.main import app[m
[32m+[m
[32m+[m[32mclient = TestClient(app)[m
[32m+[m
[32m+[m
[32m+[m[32mdef test_login_invalid_credentials():[m
[32m+[m[32m    response = client.post([m
[32m+[m[32m        "/api/v1/login",[m
[32m+[m[32m        json={[m
[32m+[m[32m            "username": "wrong",[m
[32m+[m[32m            "password": "wrong"[m
[32m+[m[32m        }[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    assert response.status_code == 401[m
     [m
\ No newline at end of file[m
[1mdiff --git a/backend/tests/test_contact.py b/backend/tests/test_contact.py[m
[1mdeleted file mode 100644[m
[1mindex e69de29..0000000[m
