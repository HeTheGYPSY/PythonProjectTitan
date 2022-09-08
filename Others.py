import random
from flask import current_app, jsonify, app


class PHlo:

    def generate_code(self):
        code = random.choice(range(100000, 999999))  # generating 6 digit random code
        return code

    def send_verification_code_phlo(self, dst_number, code, mode):
            payload = {
                "from": self.app_number,
                "to": dst_number,
                "otp": code,
                "mode": mode,
            }
            try:
                phlo = self.client_phlo.phlo.get(self.phlo_id)
                response = phlo.run(**payload)
                return response
            except Exception as e:
                print(e)
                return "Error encountered", 400

    @app.route("/checkcode/<number>/<code>")
    def check_code(number, code):
        """
        check_code(number, code) accepts a number and the code entered by the user and
        tells if the code entered for that number is correct or not
        """
        original_code = current_app.redis.get("number:%s:code" % number)
        if original_code == code:  # verification successful, delete the code
            current_app.redis.delete("number:%s:code" % number)
            return jsonify({"status": "success", "message": "codes match, number verified"}), 200,
        elif original_code != code:
            return (
                jsonify(
                    {
                        "status": "rejected",
                        "message": "codes do not match, number not verified",
                    }
                ),
                404,
            )
        else:
            return jsonify({"status": "failed", "message": "number not found"}), 500


class API:

    def generate_code(self):
        code = random.choice(range(100000, 999999))  # generating 6-digit random code
        return code

    def send_verification_code_sms(self, dst_number: str, message):
        """
        `send_verification_code` accepts destination number
        to which the message that has to be sent.

        The message text should contain a `__code__` construct
        in the message text which will be
        replaced by the code generated before sending the SMS.

        :param: dst_number
        :param: message
        :return: verification code
        """
        try:
            response = self.client.messages.create(
                src=self.app_number, dst=dst_number, text=message
            )
            print(response)
            return response
        except Exception as e:
            print(e)
            return "Error encountered", 400

    def send_verification_code_voice(self, dst_number, code):
        try:
            response = self.client.calls.create(
                from_=self.app_number,
                to_=dst_number,
                answer_url=f"https://twofa-answerurl.herokuapp.com/answer_url/{code}",
                answer_method="GET",
            )
            return response
        except Exception as e:
            print(e)
            return "Error encountered", 400

    @app.route("/checkcode/<number>/<code>")
    def check_code(self, code):
        """
        check_code(number, code) accepts a number and the code entered by the user and
        tells if the code entered for that number is correct or not.
        """

        original_code = current_app.redis.get("number:%s:code" % self)
        if original_code == code:  # verification successful, delete the code
            current_app.redis.delete("number:%s:code" % self)
            return jsonify({"status": "success", "message": "codes match, number verified"}), 200,
        elif original_code != code:
            return (
                jsonify(
                    {
                        "status": "rejected",
                        "message": "codes do not match, number not verified",
                    }
                ),
                404,
            )
        else:
            return jsonify({"status": "failed", "message": "number not found"}), 500