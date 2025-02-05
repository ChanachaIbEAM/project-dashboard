import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table

# อ่านข้อมูลจากไฟล์ Excel
file_path = '22-134Socket.xlsx'
df = pd.read_excel(file_path)

# ทำความสะอาดชื่อคอลัมน์ (ลบช่องว่าง)
df.columns = df.columns.str.strip()

# ตรวจสอบว่าคอลัมน์ 'Privote' มีอยู่ใน DataFrame หรือไม่
if 'Privote' not in df.columns:
    raise KeyError("The column 'Privote' does not exist in the DataFrame. Please check the column name.")

# ตัดคอลัมน์ที่ไม่ต้องการออก
columns_to_exclude = ['Baseline Start', 'Baseline Finish', 'Variance']
df = df[[col for col in df.columns if col not in columns_to_exclude]]

# แปลงวันที่ให้เป็น datetime object และจัดการข้อผิดพลาด
df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')

# ลบเวลาออกจากวันที่และเปลี่ยนรูปแบบเป็น dd/mm/yyyy
df['Start Date'] = df['Start Date'].dt.strftime('%d/%m/%Y')
df['End Date'] = df['End Date'].dt.strftime('%d/%m/%Y')

# สรุปข้อมูลโปรเจกต์
project_name = "22-134 Change Maker of Socket from Fukui to Unipro"
start_date = "2024-12-16"
end_date = "2025-06-01"

# คำนวณเปอร์เซ็นต์ความคืบหน้า
status_counts = df['Status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']

if not status_counts.empty:
    total_tasks = status_counts['Count'].sum()
    completed_tasks = status_counts.loc[status_counts['Status'] == 'Complete', 'Count'].sum() if 'Complete' in status_counts['Status'].values else 0
    percent_complete = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
else:
    total_tasks = 0
    completed_tasks = 0
    percent_complete = 0

# กำหนดสีสำหรับแต่ละสถานะ
color_map = {
    "Complete": "#A5D6A7",  # สีเขียวอ่อน
    "In Progress": "#FFF59D",  # สีเหลืองอ่อน
    "Not Started": "#FFABAB"  # สีแดงอ่อน
}

# กราฟวงกลม (Donut Chart) สำหรับ % Complete
fig_complete = px.pie(status_counts, values='Count', names='Status', hole=0.4,
                      color_discrete_map=color_map)
fig_complete.update_traces(
    textinfo='percent+label',
    insidetextfont=dict(color='white'),
    texttemplate='%{label}: %{percent:.1%}'
)

# กรองข้อมูลเฉพาะที่มี 'o' ในคอลัมน์ Privote สำหรับ Gantt Chart
filtered_df = df[df['Privote'] == 'o']

# Gantt Chart สำหรับ Timeline (แสดงเฉพาะข้อมูลที่กรองแล้ว)
fig_gantt = px.timeline(filtered_df, x_start='Start Date', x_end='End Date', y='Topic', color='Status',
                        color_discrete_map=color_map,
                        title='Project Timeline')
fig_gantt.update_yaxes(autorange="reversed")  # แสดง Task จากบนลงล่าง

# กราฟแท่งสำหรับสถานะโปรเจกต์
fig_status = px.bar(status_counts, x='Status', y='Count', color='Status',
                    color_discrete_map=color_map)

# สร้างแอป Dash
app = Dash(__name__)

app.layout = html.Div(style={
    'font-family': 'Arial, sans-serif',
    'backgroundColor': '#f9f9f9',
    'padding': '20px'
}, children=[
    # ชื่อ Project Dashboard ด้านบนสุด พร้อมจัดระยะห่างและขนาดฟอนต์ใหม่
    html.Div([
        html.H1('Project Dashboard', style={
            'textAlign': 'center',
            'color': '#333',
            'font-size': '2rem',
            'margin-bottom': '10px'
        }),
        html.P('Welcome to my project.', style={
            'textAlign': 'center',
            'color': '#666',
            'font-size': '1rem',
            'margin-bottom': '20px'
        })
    ]),

    # ส่วน Project Details ด้านบนสุดพร้อมไอคอนและปรับระยะห่างใหม่
# ส่วน Project Details ด้านบนสุดพร้อมไอคอนและปรับระยะห่างใหม่
html.Div([
    # ใช้ Flexbox เพื่อจัดการทั้งข้อความและรูปภาพให้อยู่ในกรอบเดียวกัน
    html.Div([
        # คอลัมน์สำหรับข้อความ Project Details
        html.Div([
            html.H3('🔍 Project Details', style={'color': '#444', 'font-weight': 'bold'}),
            html.P(f'📁 Project Name: {project_name}', style={'margin': '5px 0'}),
            html.P(f'📅 Start Date: {start_date}', style={'margin': '5px 0'}),
            html.P(f'📅 End Date: {end_date}', style={'margin': '5px 0'}),
            html.P(f'📊 Progress: {round(percent_complete, 2)}%', style={
                'margin': '5px 0',
                'font-size': '1.2rem',
                'font-weight': 'bold',
                'color': '#007BFF'
            })
        ], style={
            'flex': 1,  # ให้ข้อความใช้พื้นที่ส่วนใหญ่
        }),

        # คอลัมน์สำหรับรูปภาพ
        html.Div([
            html.Img(src='/assets/socket.png', style={
                'width': '200px',  # ขยายความกว้างของรูปภาพ
                'height': 'auto',  # ให้ความสูงปรับตามสัดส่วน
                'border-radius': '8px',  # เพิ่มมุมโค้งมนให้รูปภาพ
                'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.1)'  # เพิ่มเงาให้รูปภาพ
            })
        ], style={
            'flex-shrink': 0,  # ไม่ให้ย่อขนาดลง
            'display': "flex",
            "align-items": "center",  # จัดให้อยู่กลางในแนวตั้ง
            "justify-content": "left",  # จัดให้อยู่กลางในแนวนอน
            "height": "100%",  # ให้สูงเต็มกรอบ
        }),
    ], style={
        "display": "flex",           # ใช้ Flexbox สำหรับจัดเรียงข้อความและรูปภาพในแถวเดียวกัน
        "align-items": "center",     # จัดให้อยู่กลางในแนวตั้ง
    }),
], style={
    'backgroundColor': '#fff',
    'border-radius': '12px',
    'padding': '15px',
    'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.1)',  
    "margin-bottom": "20px"      
}),

    # ส่วน Donut Chart และ Bar Chart ในแถวเดียวกันพร้อมจัดระยะห่างใหม่
    html.Div([
        html.Div([
            dcc.Graph(figure=fig_complete)
        ], style={
            'width': '48%',
        }),

        html.Div([
            dcc.Graph(figure=fig_status)
        ], style={
            'width': '48%',
        }),
    ], style={'display': 'flex'}),

    # ส่วน Gantt Chart ด้านล่างสุดพร้อมจัดระยะห่างใหม่
    html.Div([
        dcc.Graph(figure=fig_gantt)
    ]),

    # Task Summary Table ด้านล่างสุดในกรอบ (Card)
    html.Div([
        html.H3('📋 Task Summary Report', style={'color': '#555'}),
        
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': col, 
                      'id': col} for col in df.columns],
            style_table={
                "overflowX": "auto",  
                "border-radius": "8px",
                },
            style_cell={
                "textAlign": "center",
                "padding": "8px",
                "font-size": "1rem"
            },
            style_header={
                "backgroundColor": "#f4f4f4",
                "fontWeight": "bold",
                "color": "#333"
            },
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "#f9f9f9",
                },
                {
                    # เทสีเฉพาะในคอลัมน์ Status สำหรับ Complete
                    "if": {"column_id": "Status", "filter_query": '{Status} = "Complete"'},
                    "backgroundColor": "#A5D6A7",
                    "color": "#333",
                },
                {
                    # เทสีเฉพาะในคอลัมน์ Status สำหรับ In Progress
                    "if": {"column_id": "Status", "filter_query": '{Status} = "In Progress"'},
                    "backgroundColor": "#FFF59D",
                    "color": "#333",
                },
                {
                    # เทสีเฉพาะในคอลัมน์ Status สำหรับ Not Started
                    "if": {"column_id": "Status", "filter_query": '{Status} = "Not Started"'},
                    "backgroundColor": "#FFABAB",
                    "color": "#333",
                },
            ],
        ),
    ], style={'margin-top':'20px'})
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
