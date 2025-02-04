import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table

# อ่านข้อมูลจากไฟล์ Excel
file_path = r'C:\Users\chanachai.o\vs code\22-134Socket.xlsx'
df = pd.read_excel(file_path)

# สรุปข้อมูลโปรเจกต์
project_name = "22-134 Change Maker of Socket"
start_date = "16/12/24"
end_date = "01/06/25"

# คำนวณเปอร์เซ็นต์ความคืบหน้า
status_counts = df['Status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']
total_tasks = status_counts['Count'].sum()
completed_tasks = status_counts.loc[status_counts['Status'] == 'Complete', 'Count'].sum()
percent_complete = (completed_tasks / total_tasks) * 100

# กราฟวงกลม (Donut Chart) สำหรับ % Complete
fig_complete = px.pie(status_counts, values='Count', names='Status', hole=0.4,
                      color_discrete_sequence=px.colors.qualitative.Set3)

# กราฟแท่งสำหรับสถานะโปรเจกต์
fig_status = px.bar(status_counts, x='Status', y='Count', color='Status',
                    color_discrete_sequence=px.colors.qualitative.Set3)

# สร้างแอป Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Project Dashboard', style={'textAlign': 'center'}),

    # แสดงรายละเอียดโปรเจกต์
    html.Div([
        html.H3('Detail Project:'),
        html.P(f'Project Name: {project_name}'),
        html.P(f'Start Date: {start_date}'),
        html.P(f'End Date: {end_date}'),
    ], style={'border': '1px solid #ccc', 'padding': '10px', 'margin': '10px'}),

    # แสดงเปอร์เซ็นต์ความคืบหน้า
    html.Div([
        html.H3('Project % Complete'),
        dcc.Graph(figure=fig_complete)
    ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    # แสดงสถานะโปรเจกต์
    html.Div([
        html.H3('Project Status'),
        dcc.Graph(figure=fig_status)
    ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    # ตารางรายงานสรุปงาน
    html.Div([
        html.H3('Task Summary Report'),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in df.columns],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center', 'padding': '5px'},
            style_header={
                'backgroundColor': '#f4f4f4',
                'fontWeight': 'bold'
            }
        )
    ], style={'margin': '20px'})
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)


