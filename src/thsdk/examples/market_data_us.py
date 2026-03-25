from thsdk import THS

from thsdk.examples._helpers import print_response_df


def main():
    with THS() as ths:
        response = ths.nasdaq_lists()
        if not response:
            print(f"获取纳斯达克股票列表失败: {response.error}")
            return

        symbols = response.df["代码"].head(5).tolist()
        print("示例代码:", symbols)

        market_response = ths.market_data_us(symbols, query_key="基础数据")
        if not market_response:
            print(f"查询美股市场数据失败: {market_response.error}")
            return

        print_response_df("查询结果:", market_response)


if __name__ == "__main__":
    main()
