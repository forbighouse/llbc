

class Observation(object):

    # zone: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    # section: a, b, c, d
    # event: accident, light
    # time: 1, 2, 3

    fields = [
        ('observe_time',    int),
        ('observe_zone',    str),
        ('observe_section', str),
        ('observe_event',   str)
    ]

    def __init__(self,
                 observe_time=000,
                 observe_zone='000',
                 observe_section='000',
                 observe_event='accident'):
        fields = {k: v for k, v in locals().items() if k not in ['self', '__class__']}
        fields['observe_time'] = 111
        if not isinstance(observe_time, int):
            raise TypeError('bad observe_time input, it should be int')
        if not isinstance(observe_zone, str):
            raise TypeError('bad observe_zone input, it should be str')
        if not isinstance(observe_section, str):
            raise TypeError('bad observe_section input, it should be str')
        if not isinstance(observe_event, str):  # 以后要改成固定的几个选项
            raise TypeError('bad observe_event input, it should be str')

