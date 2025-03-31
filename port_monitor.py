import psutil
import socket
from tabulate import tabulate
import sys
import os
from colorama import init, Fore, Back, Style
from datetime import datetime
import concurrent.futures
import threading

init(autoreset=True)

def print_header():
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}端口占用监控工具")
    print(f"{Fore.CYAN}检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def get_process_by_port(port):
    if not hasattr(get_process_by_port, 'process_cache'):
        get_process_by_port.process_cache = {}
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                for conn in proc.connections():
                    get_process_by_port.process_cache[conn.laddr.port] = proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    return get_process_by_port.process_cache.get(port)

def kill_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        return True
    except psutil.NoSuchProcess:
        return False

def check_single_port(port, service):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            process = get_process_by_port(port)
            if process:
                return [
                    f"{Fore.GREEN}{port}{Style.RESET_ALL}",
                    f"{Fore.YELLOW}{service}{Style.RESET_ALL}",
                    f"{Fore.RED}PID: {process.pid}{Style.RESET_ALL}",
                    f"{Fore.BLUE}{process.name()}{Style.RESET_ALL}",
                    f"{Fore.RED}已占用{Style.RESET_ALL}"
                ]
        sock.close()
    except:
        pass
    return None

def check_common_ports():
    common_ports = {
        80: "HTTP",
        443: "HTTPS",
        8080: "HTTP-Alt",
        8443: "HTTPS-Alt",
        8888: "HTTP-Alt",
        9000: "HTTP-Alt",
        3000: "Node.js/React",
        3001: "Node.js/React-Alt",
        4200: "Angular",
        5173: "Vite",
        5174: "Vite-HMR",
        8081: "React-Native",
        8082: "React-Native-Alt",
        19006: "Expo",
        5000: "Flask/Development",
        8000: "Django/Development",
        8001: "Django-Alt",
        9001: "Django-Alt",
        9090: "Go-Development",
        4000: "Phoenix/Elixir",
        4567: "Sinatra/Ruby",
        3000: "Express/Node.js",
        3001: "Express-Alt",
        4000: "NestJS",
        4200: "Laravel",
        5000: "FastAPI",
        8000: "FastAPI-Alt",
        3306: "MySQL",
        3307: "MySQL-Alt",
        5432: "PostgreSQL",
        5433: "PostgreSQL-Alt",
        27017: "MongoDB",
        27018: "MongoDB-Alt",
        6379: "Redis",
        6380: "Redis-Alt",
        1433: "MSSQL",
        1434: "MSSQL-Browser",
        1521: "Oracle",
        1522: "Oracle-Alt",
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        110: "POP3",
        143: "IMAP",
        993: "IMAP-SSL",
        995: "POP3-SSL",
        1080: "SOCKS",
        3128: "Squid",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        8080: "Proxy"
    }
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_port = {
            executor.submit(check_single_port, port, service): (port, service)
            for port, service in common_ports.items()
        }
        for future in concurrent.futures.as_completed(future_to_port):
            result = future.result()
            if result:
                results.append(result)
    return results

def print_help():
    print(f"\n{Fore.CYAN}使用说明：")
    print(f"1. 输入进程ID（PID）来终止对应的进程")
    print(f"2. 输入 'q' 退出程序")
    print(f"3. 输入 'h' 显示此帮助信息{Style.RESET_ALL}\n")

def main():
    if not is_admin():
        print(f"{Fore.RED}错误：请以管理员权限运行此程序！{Style.RESET_ALL}")
        return

    print_header()
    print(f"{Fore.YELLOW}正在检查常用端口占用情况...{Style.RESET_ALL}")
    results = check_common_ports()
    
    if not results:
        print(f"{Fore.GREEN}未发现端口占用情况。{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}端口占用情况：{Style.RESET_ALL}")
    print(tabulate(results, 
                  headers=[f"{Fore.CYAN}端口{Style.RESET_ALL}", 
                          f"{Fore.CYAN}服务{Style.RESET_ALL}", 
                          f"{Fore.CYAN}进程ID{Style.RESET_ALL}", 
                          f"{Fore.CYAN}进程名称{Style.RESET_ALL}", 
                          f"{Fore.CYAN}状态{Style.RESET_ALL}"], 
                  tablefmt="grid"))
    
    print_help()
    
    while True:
        try:
            choice = input(f"{Fore.YELLOW}请输入要终止的进程ID（输入 'q' 退出，'h' 显示帮助）: {Style.RESET_ALL}")
            if choice.lower() == 'q':
                print(f"\n{Fore.GREEN}感谢使用！再见！{Style.RESET_ALL}")
                break
            elif choice.lower() == 'h':
                print_help()
                continue
            
            pid = int(choice)
            if kill_process(pid):
                print(f"{Fore.GREEN}成功终止进程 {pid}{Style.RESET_ALL}")
                results = check_common_ports()
                print(f"\n{Fore.CYAN}更新后的端口占用情况：{Style.RESET_ALL}")
                print(tabulate(results, 
                             headers=[f"{Fore.CYAN}端口{Style.RESET_ALL}", 
                                     f"{Fore.CYAN}服务{Style.RESET_ALL}", 
                                     f"{Fore.CYAN}进程ID{Style.RESET_ALL}", 
                                     f"{Fore.CYAN}进程名称{Style.RESET_ALL}", 
                                     f"{Fore.CYAN}状态{Style.RESET_ALL}"], 
                             tablefmt="grid"))
            else:
                print(f"{Fore.RED}无法终止进程 {pid}，可能进程已经结束{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}请输入有效的进程ID{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN}感谢使用！再见！{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    main()