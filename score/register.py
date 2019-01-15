
class Register(object):

    def __init__(self, veh_id):
        self._registered_list = set()
        self._veh_id = veh_id

    def add(self, v_public_key):
        self._registered_list.add(v_public_key)

    def delete(self, v_public_key):
        self._registered_list.remove(v_public_key)

    @property
    def register_list(self):
        return self._registered_list
