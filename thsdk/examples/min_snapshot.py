from thsdk import THS
import pandas as pd
import time

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

with THS() as ths:
    code = "USZA300033"
    date = "20251225"

    response = ths.min_snapshot(code, date)
    print(f"查询历史分时快照: 代码={code}, 日期={date}")

    if not response or not response.success or response.error:
        print(f"❌ 查询失败，错误信息: {getattr(response, 'error', '未知错误')}")
    elif not response.data or len(response.data) == 0:
        print("⚠️ 未获取到分时快照数据（返回数据为空）。")
    else:
        df = response.df
        if "时间" in df.columns:
            try:
                df["时间"] = pd.to_datetime(df["时间"], unit="s", utc=True).dt.tz_convert("Asia/Shanghai")
            except Exception as ex:
                print(f"时间列转换失败: {ex}")
        # 展示前几行
        print(df)
        print(f"\n共{len(df)}条分时数据。")
        print(f"包含字段: {list(df.columns)}")

    time.sleep(1)
