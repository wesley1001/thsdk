# 本示例展示如何使用THSDK获取DDE（大单资金流向）相关数据。
# DDE（大单资金流向）用于分析个股在一定时间段内的大单资金进出情况，常用于判断主力资金动向，辅助投资决策。
# 本示例演示如何查询详细DDE数据、个股DDE统计数据，以及板块DDE资金流向数据。
from thsdk import THS
import pandas as pd
import time


# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

def pretty_print(title, df):
    print("\n" + "=" * 60)
    print(f"【{title}】")
    if df is None or df.empty:
        print("⚠️ 数据为空")
    else:
        print(f"共 {len(df)} 行, 包含字段: {list(df.columns)}")
        print(df)

    print("=" * 60 + "\n")


with THS() as ths:
    response = ths.query_data({
        "id": 200,
        "codelist": "600821,600089,600386,601618,600642,601011,601678,603181,600482,600118,600308,600863,600273,600988,601918",
        "market": "USHA",
        "datatype": "6,7,8,9,10,13,19,223,224,225,226,227,228,229,230",
        "service": "zhu",

    })
    pretty_print("dde详细数据", getattr(response, "df", None))
    time.sleep(1)

    response = ths.query_data({
        "id": 200,
        "codelist": "600821,600089,600386,601618,600642,601011,601678,603181,600482,600118,600308,600863,600273,600988,601918",
        "market": "USHA",
        "datatype": "6,7,8,9,10,13,19,592888,592890",
        "service": "zhu",

    })
    pretty_print("个股dde统计数据", getattr(response, "df", None))
    time.sleep(1)

    block_response = ths.block(0xCE5E)  # 全部概念板块
    if not block_response:
        print(f"\n❌ 概念板块获取板块数据失败: {getattr(block_response, 'error', '未知错误')}")
    else:
        df = block_response.df
        block_codes = df['代码'].astype(str).tolist()

        # 找到长度为10的元素，提取前四位和后六位
        market_codelist_map = {}
        for code in block_codes:
            if len(code) == 10:
                market = code[:4]
                codelist_code = code[4:]
                if market not in market_codelist_map:
                    market_codelist_map[market] = []
                market_codelist_map[market].append(codelist_code)

        for market, codelist in market_codelist_map.items():
            codelist_str = ",".join(codelist)
            response = ths.query_data({
                "id": 202,
                "codelist": codelist_str,
                "market": market,
                "datatype": "6,7,8,9,10,13,19,331073,68285",
                "service": "fu",
            })
            pretty_print(f"板块dde统计数据 (market={market})", getattr(response, "df", None))
            time.sleep(1)
