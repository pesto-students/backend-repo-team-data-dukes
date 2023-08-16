from api.register import register
from api.login import login
from api.password import reset_password
from api.upload import upload
from api.contacts import contacts
from api.files import getFiles
from api.oauth import oauth
from api.valid import valid
from api.profile import update

def mount_urls(router):
    router.add_api_route("/register", register, methods=["POST"])
    router.add_api_route("/login", login, methods=["POST"])
    router.add_api_route("/reset-password", reset_password, methods=["PATCH"])
    router.add_api_route("/upload-file",upload, methods=["POST"])
    router.add_api_route("/contacts", contacts, methods=["GET"])
    router.add_api_route("/get-files", getFiles, methods=["GET"])
    router.add_api_route("/oauth", oauth, methods=["POST"])
    router.add_api_route("/valid", valid, methods=["GET"])
    router.add_api_route("/update-profile", update, methods=["PATCH"])
    return router