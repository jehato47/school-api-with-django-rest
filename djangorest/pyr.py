# import pyrebase
# from datetime import date
# from pathlib import Path
# import os
# p = Path("C:/Users/kenda/PycharmProjects/djangorest")
# os.chdir(p)
#
# config = {
#     "serviceAccount": {
#         "type": "service_account",
#         "project_id": "pyrebase-fb673",
#         "private_key_id": "da778d9b9883eb1a5a95bd2f84bcab2ff612ed7c",
#         "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDpnUZk4mHp+5BE\nUBOEJ2WT6/gsxMKwP+oSohVTURU3yfGq1DfEU5B+4pIyxVIz/l/e0mnto0PPhMsY\nI0q+OZI7sthXYSYrLm6nZ411kZ9Yce7MmgOro/NtDWiWRmOuXCtsk4gD6899bAwo\ndibsOXgoFsQKSSVBpYNTsVyqORUDVDd8p1dowbMj90pwZ+o+WptzZVbRoWv8Xl6Z\nzokUkVu2sjLxgUVxEX+QDOLOXG8rO4dn3bPwrqBmT1dENcJVOeNBSJ3qu/p5Q3T2\nZdxWDu/mXCl/v6f2j+U6wUrktE0TCOV67B8cGHRULenS4Tm+LCFxSKy2nrnQzOWr\n4WOLMDuXAgMBAAECggEAHgBpOG6MVZDNk8BW6Utn86nDyvgP6rOim3b+Vx9cIriI\nFUDA0rFKpsjxLp0BtBSwejy6ht7HSCDNNlHd+PUKzyjmOL6MuNHzOwOE+rrTZHfp\nS5Rh8UqSaghlTJtIlO1YVE7UEnDXyks0eoPF9uNgh4F49rszEi2v4nEuLdw70xvg\nXami6nM///gt2RjDFziqbLjh2Y/Oa3eRZ9PRYlF+XSA9KOBZbAf4Jy8rAgQ9aTGu\nIcaLdYkCG4RwBeRZ6uIgK9Uq9v63ivRh4A9LmYepkgZa/9djTRd3wSLdEVEy8UdQ\nNKEnCcb1Y0WAW0RY9Ok6sHkEX+CF3z3XeU+A9y6eGQKBgQD2gGOehWcHq81MALxs\nqbxV5U/LR1NB5P0mPwT9pLJljnJL2U1eBf8Sx4tugu/0kimTTScY7oTLoPkVai3P\n0KncksZxdcz6NQ1pj2Kqwo0IqK17IGgyF5XyhKNMlvJ5FK4F0kS9dIfYRJBZBkcm\nLhXVTZX9Y/GGtRJI9XmNcN1Z6QKBgQDyncK1X1OZeKz4/5zDZujk3VMqpn8irTYn\ngdHrAFZqpgigmdZdRTjV1kJlKCX5zS+ZgqQTIsFwA/5ScvQbPQGw0TvXf6pCPAgH\nlj54b8Z9Q604bTrs6+zzIlHwPu+sSRxeTKX+Dtv2GhUFtj1Ucs484SP5vXD/d+ZE\nto7xiGX5fwKBgQCaWciHQYdDQWu61Jcn/5zDuGQfqJjUoRt28G0imhdvCiQ9pGMS\npfSTgMmpOGoincdUyjHaJbiXfUObCjKHd2R1jp6d+yKP5dpxJ+yjelEvg9elSqSU\nATrOcgmC8t3/vVg+ouySKT7KyBwO8qRonuDjAMMTuJpLPGSntLYZP/wKyQKBgQCU\nf0062EMCD6PHsCSSUT3BP1p1I31zixM3cTU8InPCSSfErQRRCFp2P/NZmQ5NbHJz\nAkxMzhwZ5MfYTTXuKhQL1rVK/IAIlFfR1PsdmkSiTTcL74d+lhTs6BfA9bSa/hDY\nAxAihZPKeUJewaGeO7rR9nefl30/UHLnodmyKmtIHwKBgGfy7YSR5ebV1/EqS6co\njQGHU9nm8APPo16J9tPGRkhvECbGWuujVM8kCamow5updNe77KKJlGUmFDOpttPs\nNTAahFJPZu7/3icZp/pIQNYthbhbSLY6m4isL6YXzcepYODYaj5oR55/qobCT8EI\nos96lKuP1Irp8oTrgY25ktvm\n-----END PRIVATE KEY-----\n",
#         "client_email": "firebase-adminsdk-ktsid@pyrebase-fb673.iam.gserviceaccount.com",
#         "client_id": "105154356533456842419",
#         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#         "token_uri": "https://oauth2.googleapis.com/token",
#         "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#         "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ktsid%40pyrebase-fb673.iam.gserviceaccount.com"
#     },
#     "apiKey": "AIzaSyDaZr5P5xsWAHZpUpFRAN22quyeZTahhEc",
#     "authDomain": "pyrebase-fb673.firebaseapp.com",
#     "databaseURL": "https://pyrebase-fb673.firebaseio.com",
#     "projectId": "pyrebase-fb673",
#     "storageBucket": "pyrebase-fb673.appspot.com",
#     "messagingSenderId": "1027924436984",
#     "appId": "1:1027924436984:web:4afff6bfe0768cd1c0580d",
#     "measurementId": "G-M9ZRB6J6QT"
# }
#
# f = pyrebase.initialize_app(config=config)
#
#
# # pos = "{}.sqlite3".format(db)
# # poc = "{}/{}/{}.sqlite3".format(db, date.today(), db)
# def upload(poc, pos):
#     storage = f.storage()
#     storage.child(poc).put(pos)
#
#
# def download(poc, pos):
#     storage = f.storage()
#     storage.child(poc).download(pos)
#
#
# def get(db):
#     storage = f.storage()
#     dbs = [str(i).split("/")[1] for i in storage.child(db).list_files() if str(i).split("/")[2].startswith(db)]
#     return dbs
#
