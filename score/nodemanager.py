

class ServiceNode(object):

    fields = [
        ('node_type', int), # 0：vehicle，1：RSU，-1：raise error
        ('veh_id', str),
        ('longitude', int),
        ('latitude', int),
        ('observe_vehs', list),
        ('current_time', int)
    ]

    def __init__(self,
                 node_type=-1,
                 veh_id='000',
                 longitude=0,
                 latitude=0,
                 observe_vehs=None,
                 current_time=None
                 ):
        if not node_type == 1 or node_type == 0:
            raise TypeError('bad node_type, please set it to 0(vehicle) or 1(RSU)')
        else:
            self._node_type = node_type
        if not isinstance(veh_id, str):
            raise TypeError('bad veh_id, it should be str')
        else:
            self._veh_id = veh_id
        if not isinstance(longitude, int):
            raise TypeError('bad longitude, it should be int')
        else:
            self._longitude = longitude
        if not isinstance(latitude, int):
            raise TypeError('bad latitude, it should be int')
        else:
            self._latitude = latitude
        if not isinstance(observe_vehs, list):
            raise TypeError('bad observe_vehs, it should be list')
        else:
            self._observe_vehs = observe_vehs
        if not observe_vehs:
            observe_vehs = []
            self._observe_vehs = observe_vehs
        elif not isinstance(observe_vehs, list):
            raise TypeError('bad observe_vehs, it should be list')
        if not isinstance(current_time, int):
            raise TypeError('bad current_time, it should be int')
        else:
            self._current_time = current_time

    def show_fields(self):
        print(self._node_type, self._veh_id, self._longitude, self._latitude,self._observe_vehs,self._current_time)

    @property
    def observe_vehicle(self):
        return self._observe_vehs

    @property
    def veh_id(self):
        return self._veh_id

    @ property
    @def latitude(self):
        return self._latitude

    @ property
    @def longitude(self):
        return self._latitude

    @observe_vehicle.setter
    def observe_vehicle(self, observe_vehs):
        if isinstance(observe_vehs, str):
            self._observe_vehs.append(observe_vehs)
            print('I can see ', observe_vehs)
        else:
            raise TypeError('observe_vehicle should be str')



class BlockNode(object):
    pass
