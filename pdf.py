from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import subprocess

def create_sales_report():
    # Example sales data
    sales_data = [
        {"item_name": "Product A", "quantity_sold": 5, "unit_price": 10, "total_amount": 50},
        {"item_name": "Product B", "quantity_sold": 3, "unit_price": 15, "total_amount": 45},
        # Add more sales records as needed
    ]

    # Specify the file path for the PDF
    file_path = "sales_report.pdf"

    # Create a PDF file
    pdf = SimpleDocTemplate(file_path, pagesize=letter)

    # Define table data and styles
    table_data = [["Item Name", "Quantity Sold", "Unit Price", "Total Amount"]]

    for sale in sales_data:
        table_data.append([
            sale["item_name"],
            sale["quantity_sold"],
            sale["unit_price"],
            sale["total_amount"]
        ])

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Create a title for the report
    title_style = getSampleStyleSheet()["Title"]
    title = Paragraph("<u>Sales Report</u>", title_style)

    # Create a table and apply styles
    table = Table(table_data)
    table.setStyle(style)

    # Build the PDF
    pdf.build([title, table])

    # Open the PDF file
    subprocess.run(["xdg-open", file_path], check=True)

if __name__ == "__main__":
    create_sales_report()