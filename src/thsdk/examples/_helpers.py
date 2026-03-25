import pandas as pd

from thsdk import THS


def print_response_df(title: str, response):
    print(title)
    if not response:
        print(f"查询失败: {response.error}")
        return None

    df = response.df
    if isinstance(df, pd.DataFrame):
        if df.empty:
            print("没有数据")
        else:
            print(df)
    else:
        print(response.data)
    return df


def run_market_data_example(
    list_loader_name: str,
    query_method_name: str,
    title: str,
    query_key: str = "基础数据",
    sample_size: int = 5,
):
    with THS() as ths:
        list_response = getattr(ths, list_loader_name)()
        if not list_response:
            print(f"获取列表失败: {list_response.error}")
            return

        codes = list_response.df["代码"].head(sample_size).tolist()
        print(f"{title}示例代码: {codes}")

        market_response = getattr(ths, query_method_name)(codes, query_key=query_key)
        if not market_response:
            print(f"查询失败: {market_response.error}")
            return

        df = market_response.df
        if isinstance(df, pd.DataFrame):
            print(df)
            print(f"\n查询成功，返回 {len(df)} 条数据。")
        else:
            print(market_response.data)
