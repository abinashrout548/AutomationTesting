from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("reports/Test_Report.pdf")
styles = getSampleStyleSheet()

story = []

story.append(Paragraph("Digital Register Automation Report", styles["Heading1"]))

for r in results:
    story.append(
        Paragraph(
            f"{r['name']} : {r['status'].upper()}",
            styles["Normal"]
        )
    )

doc.build(story)