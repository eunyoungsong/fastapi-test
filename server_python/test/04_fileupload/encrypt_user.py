#!/bin/python3
###############################################################################
# Copyright (C) 2021-2022 SMSOFT smsoft@smsoft.co.kr
#
# This file is part of sm-mission/remostaion
#
# sm-mission can not be copied and/or distributed without the
# express permission of SMSOFT
###############################################################################

import json
from passlib.context import CryptContext
from typing import Optional

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encrypt_user(username: str, new_password: Optional[str] = None, new_password_again: Optional[str] = None, email: Optional[str] = None, full_name: Optional[str] = None):
    # 정보 변경
    if new_password is None and new_password_again is None :
        with open("user_db.json", "r") as json_file:
            json_data = json.load(json_file)

            json_data[username]["email"] = email
            json_data[username]["full_name"] = full_name

            with open("./user_db.json", "w", encoding="utf-8") as json_file:
                json.dump(json_data, json_file, indent="\t")            
            return json_data[username];

    # 비밀번호 변경
    else:
        if new_password != new_password_again:
            raise ValueError('bad password')

        user_db = {
            username: {
                "username": username,
                "hashed_password": crypt_context.hash(new_password),
                "disabled": False
            }
        }

        with open("user_db.json", "w") as json_file:
            json.dump(user_db, json_file, indent="\t")


if __name__ == '__main__':
    try:
        print("testing... correct password")
        encrypt_user("admin", "password2", "password2")
    except ValueError as e:
        print('exception', e)

    try:
        print("testing... bad password")
        encrypt_user("admin", "password1", "password2")
    except ValueError as e:
        print('except', e)
