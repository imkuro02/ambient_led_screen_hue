from screeninfo import get_monitors

def get_monitor(monitor_name):
    monitor = None
    monitors = get_monitors()
    for m in monitors:
        if monitor_name == m.name:
            monitor = m

    if monitor == None :
        names = []
        for m in monitors:
            names.append(m.name)
        print(f'could not fint monitor {MONITOR_NAME}')  
        print(f'monitor names available:{names}')

    print(f'selected monitor {monitor.name}')
    return monitor

if __name__ == '__main__':
    MONITOR_NAME = 'DP-2!'
    MONITOR = get_monitor(MONITOR_NAME)
