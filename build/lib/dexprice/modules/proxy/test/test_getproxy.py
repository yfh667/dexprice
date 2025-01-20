import modules.proxy.getproxy as  getproxy

if __name__ == "__main__":
    # 设置要检查的端口范围
    start_port = 50000
    numner = 30
    # end_port = 30020
    # 获取可用端口列表
    available_ports = getproxy.check_open_ports(start_port, numner)

    print("可用端口:", available_ports)
