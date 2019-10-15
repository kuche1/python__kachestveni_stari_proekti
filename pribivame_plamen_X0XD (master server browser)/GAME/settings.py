import os


if not os.path.isdir('settings'):
    os.mkdir('settings')

def get(name,defa):
    try:
        f = open('settings/%s.txt'%(name),'r')
    except FileNotFoundError:
        f = open('settings/%s.txt'%(name),'w')
        f.write(defa)
        f.close()
        return defa
    else:
        data = f.read()
        f.close()
        return data

def get_bool(name,defa):
    d = get(name,defa)
    return d == 'True'

def get_int(name,defa):
    data = get(name,defa)
    return int(data)

def get_str(name,defa):
    return get(name,defa)


def get_dedicated_server_port():
    return get_int('dedicated_server_port','27015')

def get_fullscreen():
    return get_bool('fullscreen','False')

def get_master_server_ip():
    return get_str('master_server_ip','78.90.45.230')

def get_master_server_port():
    return get_int('master_server_port','26999')

def get_res_x():
    return get_int('res_x','800')

def get_res_y():
    return get_int('res_y','600')




