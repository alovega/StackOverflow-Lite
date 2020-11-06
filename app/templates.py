"""
templates
"""

TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "StackOverflow-Lite",
        "description": "A  platform for asking and answering questions \
        that provides users with the ability to post questions \
        and also to answer all posted questions."

    },
    "securityDefinitions": {
        "TokenHeader": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"

        }
    },
    "definitions": {
        "User_sign_up": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string"
                },
                "username": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                }
            }
        },
        "User_login": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                }

            }
        },
        "Post_question": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                }

            }
        },
        "Answers": {
            "type": "object",
            "properties": {
                "answer": {
                    "type": "string"
                }
            }
        }
    }
}
