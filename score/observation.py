

class Observation(object):
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
        print(fields['observe_event'])



        # print(fields)

# def set_observation(obs):
#     ob1 = Observation()
#     ob1.