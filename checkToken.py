import threading
import requests
import concurrent.futures
import json  # 导入 json 模块

# 代币合约地址（目标链上的合约地址）
token_address = ''

def read_addresses_from_file(file_path):
    addresses = []
    with open(file_path, 'r') as file:
        for line in file:
            address = line.strip()  # 去除行尾的换行符和空白字符
            addresses.append(address)
    return addresses

# 从文件中获取要检查的地址列表
addresses_to_check = read_addresses_from_file('address.txt')

def check_token_balance(address):
    try:
        # 构建代币查询URL
        query_url = f'https://xxxxx/{address}/tokens?type=URC-721'


        print(query_url)
        # 发送HTTP请求查询代币
        response = requests.get(query_url)

        # 检查HTTP状态码
        if response.status_code == 200:
            try:
                # 解析响应数据
                data = response.json()
                # 检查是否存在URC-721代币
                items = data.get('items', [])
                has_token = any(item.get('value') == '1' for item in items)

                # 决定将地址存储在哪个文件中
                if has_token:
                    with open('address_with_token.txt', 'a') as file:
                        file.write(address + '\n')
                else:
                    with open('address_without_token.txt', 'a') as file:
                        file.write(address + '\n')

                # 打印结果
                if has_token:
                    print(f'{address} 持有URC-721代币')
                else:
                    print(f'{address} 不持有URC-721代币')
            except json.JSONDecodeError:
                print(f'无效的JSON响应数据：{response.text}')

        elif response.status_code == 404:
            with open('address_without_token.txt', 'a') as file:
                file.write(address + '\n')
                print(f'{address} 不持有URC-721代币')

        else:
            print(f'HTTP请求失败，状态码: {response.status_code}')


    except Exception as e:
        # 发生错误时记录到日志文件
        with open('error_log.txt', 'a') as error_log:
            error_log.write(f'Error for address {address}: {str(e)}\n')
        print(f'发生错误：{e}')

# 使用线程池管理线程并发执行
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # 提交任务给线程池
    futures = [executor.submit(check_token_balance, address) for address in addresses_to_check]
    # 等待所有任务完成
    concurrent.futures.wait(futures)

print('所有地址检查完成')
