cities_data = {
    "Beijing": {
        "sensor_01": {"temp": 25, "humidity": 30},
        "sensor_02": {"temp": 26, "humidity": 32}
    },
    "Shanghai": {
        "sensor_01": {"temp": 28, "humidity": 80}
    }
}


# 打印每个城市的每个传感器的温度

for city_name,city_info in cities_data.items():
    print(f"{city_name}:")
    for sensor_id,sensor_info in city_info.items():
        print(f"  - {sensor_id}: {sensor_info['temp']}")



# 问题分解
datas = [
    {"broker":"HK", "subject":"", "direction":""},
    {"broker": "SG", "subject": "", "direction": ""}
]

config = {
    "subject": {"enumerate":['正股', '期权', '期货']},
    "direction": {"enumerate":["buy", "sell"]}
}

datas = [
    {"broker":"HK", "subject":"正股", "direction":"buy"},
    {"broker": "HK", "subject": "正股", "direction": "sell"},
    {"broker": "HK", "subject": "期权", "direction": "buy"},
    {"broker": "HK", "subject": "期权", "direction": "sell"},
    {"broker": "HK", "subject": "期货", "direction": "buy"},
    {"broker": "HK", "subject": "期货", "direction": "sell"},
    {"broker": "SG", "subject": "正股", "direction": "buy"},
    {"broker": "SG", "subject": "正股", "direction": "sell"},
    {"broker": "SG", "subject": "期权", "direction": "buy"},
    {"broker": "SG", "subject": "期权", "direction": "sell"},
    {"broker": "SG", "subject": "期货", "direction": "buy"},
    {"broker": "SG", "subject": "期货", "direction": "sell"},
]

for data in datas:
    for i in range(6):
        for factor,factor_info in config.items():
            data[factor] = factor_info["enumerate"][i%len()]