# import os
# # # import pyrebase
# # # import jwt
# # # firebaseConfig = {
# # #     "apiKey": "AIzaSyBYiKRs-fIsA_-YmwWpSd7jRy9gVeUbbL0",
# # #     "authDomain": "divan-2e324.firebaseapp.com",
# # #     "projectId": "divan-2e324",
# # #     "storageBucket": "divan-2e324.appspot.com",
# # #     "messagingSenderId": "996229135049",
# # #     "appId": "1:996229135049:web:4419780bf7d9193b94ab18",
# # #     "measurementId": "G-EYEC03X8LF",
# # #     "databaseURL": ""
# # # }

# # # firebase = pyrebase.initialize_app(firebaseConfig)
# # # auth = firebase.auth()
# # # id_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjNmNjcyNDYxOTk4YjJiMzMyYWQ4MTY0ZTFiM2JlN2VkYTY4NDZiMzciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZGl2YW4tMmUzMjQiLCJhdWQiOiJkaXZhbi0yZTMyNCIsImF1dGhfdGltZSI6MTY2NjYyNDE3NSwidXNlcl9pZCI6InphZTN6bXFFRm1OaWYyaGNZYXNPckhHdHBoRTMiLCJzdWIiOiJ6YWUzem1xRUZtTmlmMmhjWWFzT3JIR3RwaEUzIiwiaWF0IjoxNjY2NjI0MjE4LCJleHAiOjE2NjY2Mjc4MTgsImVtYWlsIjoiYWhtYWQuaGFqcWFzZW1AaG90bWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiYWhtYWQuaGFqcWFzZW1AaG90bWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.dXwneafAYUkoC5rTrLawZIHEfc5ELe6EcVFWNSjFsSuRtMdo5h0hjjK5mJ6Rj31atzdWo7K5pMVjbRS-5D_NFCxlNGi74WvuzumSlICxKMl18Q52jWF_QZLbIc19sTkaTYpulQckx-N8VTlaL36GM_BRyA0vVj3R-BT0cPlo-Rb8iOtXtm-BhSEMSBDoxz8B0Zdxs6m_PnbTk9fWYJV-LuIB4kcbveZuWZV3BuKEVcAbf4ISKaedr5sD0mUMtJ1yQrJCS8g0kkLZG33-cpKdHU3qcBU2GFQNNaGmvSFniqVJ6tlwk-LHCYqorN4kYxhioxdpHyDzR14t0I2rC_jd_A"
# # # decode = jwt.decode(id_token, options={"verify_signature": False})
# # # print(decode.get('user_id'))
# # def do_something(f):
# #     def internal_function():
# #         print("ahmad")
# #         f()
# #     return internal_function


# # @do_something
# # def printB():
# #     print("abed")


# # printB()

# #print('divan.json', os.path.basename(__file__))
# print(os.path.abspath("divan.json"))


# Python program to illustrate destructor
class Employee:

    # Initializing
    def __init__(self):
        print('Employee created.')

    # Deleting (Calling destructor)
    def __del__(self):
        print('Destructor called, Employee deleted.')


obj = Employee()
del obj
