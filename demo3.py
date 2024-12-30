import streamlit as st
import pandas as pd
import sqlite3

# 连接到SQLite数据库
def connect_db():
    conn = sqlite3.connect('osm.db')
    return conn

# 从库存清单表单中获取数据
def get_inventory_data(conn):
    query = "SELECT DISTINCT 类别, 名称, 规格, 单位 FROM 库存清单"
    df = pd.read_sql_query(query, conn)
    return df

# 初始化 session_state
if 'rows' not in st.session_state:
    st.session_state.rows = []

# 连接数据库并获取数据
conn = connect_db()
df = get_inventory_data(conn)
# st.write(df)
conn.close()

tab1, tab2 = st.tabs(["办公品领用表单", "库存清单"])

st.write('hello')

with tab1:
    # 获取类别选项
    categories = df['类别'].unique().tolist()
    categories.insert(0, '')  # 添加空选项

    # 将输入框分为四列
    col1, col2, col3, col4 = st.columns(4)

    with st.container():
        # 选择类别
        with col1:
            selected_category = st.selectbox("类别", categories, index=0)

        # 根据类别选择名称选项
        if selected_category:
            names = df[df['类别'] == selected_category]['名称'].unique().tolist()
            names.insert(0, '')  # 添加空选项
        else:
            names = ['']

        # 选择名称
        with col2:
            selected_name = st.selectbox("名称", names, index=0)

        # 数量输入
        with col3:
            quantity = st.number_input("数量", min_value=0)

        # 单位选择
        with col4:
            if selected_category and selected_name:
                units = df[(df['类别'] == selected_category) & (df['名称'] == selected_name)]
                if not units.empty:
                    main_unit = units['单位'].iloc[0]
                    selected_unit = main_unit  # 直接使用主单位
                else:
                    selected_unit = ''
            else:
                selected_unit = ''

        # 显示单位
        st.write(f"单位: {selected_unit}")

        # 添加行按钮
        if st.button("选取办公用品"):
            if selected_category and selected_name and quantity and selected_unit:
                new_row = {
                    '类别': selected_category,
                    '名称': selected_name,
                    '数量': quantity,
                    '单位': selected_unit
                }
                st.session_state.rows.append(new_row)
                st.success("已添加！")
            else:
                st.error("请填写所有字段。")

        # 显示当前所有行，并使用可编辑的 DataFrame
        if st.session_state.rows:
            st.write("当前领用明细：")
            
            # 创建 DataFrame
            df_rows = pd.DataFrame(st.session_state.rows)
            
            # 使用 st.data_editor 显示可编辑的 DataFrame，允许删除行
            edited_df = st.data_editor(df_rows, num_rows="dynamic", key='editable_df')
            
            # 更新 session_state.rows 以与 edited_df 同步
            st.session_state.rows = edited_df.to_dict(orient='records')
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                user = st.text_input(label="领用人")
            with col2:
                departments = ['','生产', '质量', '工艺', '运营', '仓储']
                department = st.selectbox(label="部门", options=departments)
            with col3:
                date = st.date_input(label="领用日期")
            with col4:
                remarks = st.text_input(label='备注')
            
            # 提交表单按钮
            if st.button("确认领取"):
                if not user:
                    st.error("请填写领用人。")
                elif not department:
                    st.error("请填写部门。")
                else:
                    # 模拟提交成功
                    st.success("提交成功！")
                    st.write("提交的数据：")
                    st.write(edited_df)
                    
        else:
            st.info("尚未选择办公用品。")
            
with tab2:
    st.subheader('库存清单',divider='rainbow')
    st.write(df)  # 显示库存清单