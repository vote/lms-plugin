import json
import os

from tempfile import mkdtemp
from urllib.parse import urlencode
from flask import Flask, jsonify, render_template, request, url_for
from flask_caching import Cache
from pylti1p3.contrib.flask import (
    FlaskOIDCLogin,
    FlaskMessageLaunch,
    FlaskRequest,
    FlaskCacheDataStorage,
)
from pylti1p3.tool_config import ToolConfDict
from pylti1p3.registration import Registration
from werkzeug.middleware.proxy_fix import ProxyFix


def get_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    config = {
        "CACHE_TYPE": "simple",
        "CACHE_DEFAULT_TIMEOUT": 600,
        "SESSION_TYPE": "filesystem",
        "SESSION_FILE_DIR": mkdtemp(),
    }
    app.config.from_mapping(config)

    return app


def get_tool_conf():
    lti_config_path = os.path.join(app.root_path, "configs", "lti.json")
    config = json.load(open(lti_config_path))
    tool_conf = ToolConfDict(config)

    public_key = os.environ["PUBLIC_KEY"]
    private_key = os.environ["PRIVATE_KEY"]

    for iss, clients in tool_conf._config.items():
        for client in clients:
            tool_conf.set_public_key(iss, public_key, client_id=client["client_id"])
            tool_conf.set_private_key(iss, private_key, client_id=client["client_id"])

    return tool_conf


app = get_app()
cache = Cache(app)
tool_conf = get_tool_conf()


class ExtendedFlaskMessageLaunch(FlaskMessageLaunch):
    # ignore the deployment ID
    # https://github.com/dmitry-viskov/pylti1.3/issues/2#issuecomment-524109023
    def validate_deployment(self):
        return self


def get_launch_data_storage():
    return FlaskCacheDataStorage(cache)


def get_jwk_from_public_key(key_name):
    key_path = os.path.join(app.root_path, "configs", key_name)
    f = open(key_path, "r")
    key_content = f.read()
    jwk = Registration.get_jwk(key_content)
    f.close()
    return jwk


@app.route("/login/", methods=["GET", "POST"])
def login():
    launch_data_storage = get_launch_data_storage()

    flask_request = FlaskRequest()
    target_link_uri = flask_request.get_param("target_link_uri")
    if not target_link_uri:
        raise Exception('Missing "target_link_uri" param')

    oidc_login = FlaskOIDCLogin(
        flask_request, tool_conf, launch_data_storage=launch_data_storage
    )
    return oidc_login.enable_check_cookies().redirect(target_link_uri)


@app.route("/launch/", methods=["POST"])
def launch():
    flask_request = FlaskRequest()
    launch_data_storage = get_launch_data_storage()
    message_launch = ExtendedFlaskMessageLaunch(
        flask_request, tool_conf, launch_data_storage=launch_data_storage
    )
    message_launch_data = message_launch.get_launch_data()

    query = urlencode(
        {
            "first_name": message_launch_data.get("given_name", ""),
            "last_name": message_launch_data.get("family_name", ""),
            "email": message_launch_data.get("email", ""),
        }
    )
    return render_template("index.html", query=query)


@app.route("/jwks/", methods=["GET"])
def get_jwks():
    return jsonify({"keys": tool_conf.get_jwks()})


# https://canvas.instructure.com/doc/api/file.lti_dev_key_config.html#configuring-the-tool-in-canvas
@app.route("/config/canvas.json", methods=["GET"])
def canvas_config():
    target_link_uri = url_for("launch", _external=True)
    icon_url = "https://www.voteamerica.com/img/apple-touch-icon.png"

    return jsonify(
        {
            "title": "VoteAmerica",
            "description": "Register to vote",
            "oidc_initiation_url": url_for("login", _external=True),
            "target_link_uri": target_link_uri,
            "extensions": [
                {
                    "domain": request.host,
                    "tool_id": "voteamerica",
                    "platform": "canvas.instructure.com",
                    "privacy_level": "public",
                    "settings": {
                        "text": "VoteAmerica",
                        "icon_url": icon_url,
                        "placements": [
                            {
                                "text": "VoteAmerica",
                                "placement": "user_navigation",
                                "message_type": "LtiResourceLinkRequest",
                                "target_link_uri": target_link_uri,
                                "canvas_icon_class": "icon-lti",
                            }
                        ],
                    },
                }
            ],
            "privacy_level": "public",
            "icon_url": icon_url,
            "public_jwk_url": url_for("get_jwks", _external=True),
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9001))
    app.run(host="0.0.0.0", port=port)
