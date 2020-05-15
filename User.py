from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
import json
import uuid
from flask_login._compat import unicode
import time
from otp import OTPPreset
from keychain import KeyChainStorage
PROFILES = "profiles.json"


class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.password_hash = self.get_password_hash()
        self.id = self.get_id()
        self.seed = self.get_dynamic_seed()
        self.keychain = self.get_keychain()

    def register_user(self, password):
        """save user name, id and password hash to json file
        
        :return dynamic seed
        """
        with open(PROFILES) as f:
            try:
                profiles = json.load(f)
            except ValueError:
                profiles = {}
        if self.username in profiles.keys():
            raise Exception("username has been registered")
        # sha256 with 16 bits salt 
        self.password_hash = generate_password_hash(password,salt_length=16)
        self.keychain = KeyChainStorage.create_new_keychain()
        self.seed = self.dynamic_seed()
        with open(PROFILES,'w') as f:
            profiles[self.username] = [self.password_hash,self.id,self.seed,self.keychain]
            f.write(json.dumps(profiles))

    def dynamic_seed(self):
        """save dynamic seed to json file
        
        :return seed: the random dynamic seed
        """
        seed = OTPPreset.generate_seed()
        # windows
        OTPPreset.get_OTP_client_win(seed,".\\temp\\"+self.username+".py")
        # android
        # OTPPreset.get_OTP_client_android(seed,".\\temp\\"+self.username+".apk")
        return seed

    def verify_password(self, password, dynamic):
        if self.password_hash is None or self.seed is None:
            return False
        return check_password_hash(self.password_hash, password) and self.check_dynamic(dynamic)

    def check_dynamic(self,dynamic):
        # (unixtime%1000 /30)^2 *seed_token %1000000
        if self.seed is None:
            return False
        return OTPPreset.check(self.seed, dynamic)

    def get_dynamic_seed(self):
        """try to get dynamic seed from file.

        :return seed: if the there is corresponding user in
                the file, return seed.
                None: if there is no corresponding user, return None.
        """
        try:
            with open(PROFILES) as f:
                user_profiles = json.load(f)
                user_info = user_profiles.get(self.username, None)
                if user_info is not None:
                    return user_info[2]
        except IOError:
            return None
        except ValueError:
            return None
        return None
    
    def get_keychain(self):
        """try to get keychain file name from file.

        :return keychain: if the there is corresponding user in
                the file, return keychain file name.
                None: if there is no corresponding user, return None.
        """
        try:
            with open(PROFILES) as f:
                user_profiles = json.load(f)
                user_info = user_profiles.get(self.username, None)
                if user_info is not None:
                    return user_info[3]
        except IOError:
            return None
        except ValueError:
            return None
        return None

    def get_password_hash(self):
        """try to get password hash from file.

        :return password_hash: if the there is corresponding user in
                the file, return password hash.
                None: if there is no corresponding user, return None.
        """
        try:
            with open(PROFILES) as f:
                user_profiles = json.load(f)
                user_info = user_profiles.get(self.username, None)
                if user_info is not None:
                    return user_info[0]
        except IOError:
            return None
        except ValueError:
            return None
        return None

    def get_id(self):
        """get user id from profile file, if not exist, it will
        generate a uuid for the user.
        """
        if self.username is not None:
            try:
                with open(PROFILES) as f:
                    user_profiles = json.load(f)
                    if self.username in user_profiles:
                        return user_profiles[self.username][1]
            except IOError:
                pass
            except ValueError:
                pass
        return unicode(uuid.uuid4())
    
    def get_dynamic_passcode_client_android(self):
        """generate an OTP apk for user, returns: file name to the apk
         Note: will always generate an apk on each call
         Note: requires -nix and java environment
        """
        if self.seed is None:
            return None
        #can use designated_name="xx" to specify file name
        return OTPPreset.get_OTP_client_android(self.seed)
    
    def get_dynamic_passcode_client_windows(self):
        """generate an OTP .py for user, returns: file name to the .py
         Note: will always generate an apk on each call
         Note: requires python environment
        """
        if self.seed is None:
            return None
        #can use designated_name="xx" to specify file name
        return OTPPreset.get_OTP_client_win(self.seed)
    
    def get_keychain_items(self):
        """get a list of items from user's keychain storage
        every item in the list is a tuple(uuid, weburl, username, password, comments)
        """
        if self.keychain is None:
            return None
        return KeyChainStorage.get_keychain_item_list(self.keychain)

    @staticmethod
    def get(user_id):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        if not user_id:
            return None
        try:
            with open(PROFILES,'r',encoding='utf-8') as f:
                user_profiles = json.load(f)
                for user_name, profile in user_profiles.items():
                    if profile[1] == user_id:
                        return User(user_name)
        except Exception as e:
            return None
        return None
