import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table
import dash_html_components as html

# อ่านข้อมูลจากไฟล์ Excel
file_path = '22-134Socket.xlsx'
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
                      color_discrete_sequence=px.colors.qualitative.Set2)

# กราฟแท่งสำหรับสถานะโปรเจกต์
fig_status = px.bar(status_counts, x='Status', y='Count', color='Status',
                    color_discrete_sequence=px.colors.qualitative.Set2)

# สร้างแอป Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Project Dashboard', style={
        'textAlign': 'center', 'color': '#333', 'font-family': 'Helvetica, Arial, sans-serif', 'font-size': '2.5rem'}),

    # แสดงรายละเอียดโปรเจกต์
    html.Div([
        html.H3('Project Details:', style={'color': '#555', 'font-weight': '500'}),
        html.P(f'Project Name: {project_name}', style={'color': '#444', 'font-size': '1.2rem'}),
        html.P(f'Start Date: {start_date}', style={'color': '#444', 'font-size': '1.2rem'}),
        html.P(f'End Date: {end_date}', style={'color': '#444', 'font-size': '1.2rem'}),
    ], style={
        'backgroundColor': '#fff', 'border': '1px solid #ddd', 'padding': '15px', 'border-radius': '8px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'margin': '20px 0'
    }),

    # ไฮไลท์ "Summary" และช่อง Progress
    html.Div([
        html.H3('Summary:', style={'backgroundColor': '#f3f4a9', 'color': '#d9534f', 'font-weight': '500', 'padding': '5px'}),
        
        # แสดงเปอร์เซ็นต์ความคืบหน้า
        html.P(f'Project % Complete: {percent_complete:.2f}%', style={'color': '#444', 'font-size': '1.2rem'}),
        
        # แสดงสถานะโปรเจกต์
        html.Div([ 
            html.P(f'Status: {project_name}', style={'font-size': '1.2rem', 'color': '#444'})
        ], style={'margin': '10px 0'})

    ], style={'margin': '20px'}),

    # ตารางรายงานสรุปงาน
    html.Div([
        html.H3('Task Summary Report', style={'backgroundColor': '#f3f4a9', 'color': '#d9534f', 'font-weight': '500', 'padding': '5px'}),
        
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in df.columns],
            style_table={'overflowX': 'auto', 'border-radius': '8px'},
            style_cell={'textAlign': 'center', 'padding': '8px', 'font-size': '1rem'},
            style_header={
                'backgroundColor': '#f4f4f4', 'fontWeight': 'bold', 'color': '#333'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f9f9f9',
                },
                {
                    'if': {
                        'column_id': 'Mark',  # การเปลี่ยนสีวงกลมตามค่าในคอลัมน์ Mark
                    },
                    'backgroundColor': 'var(--circle-color)', 
                    'border-radius': '50%',
                    'width': '25px',
                    'height': '25px',
                }
            ],
        )
    ], style={'margin': '20px'})
], style={'font-family': 'Helvetica, Arial, sans-serif', 'backgroundColor': '#f8f8f8', 'padding': '20px'})

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)




