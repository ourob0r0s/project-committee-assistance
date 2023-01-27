from app import app, db
from app.models import User,Faculty_member,Student,Proposal,Group,Individual_report,Group_report


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Student': Student, 'Faculty  member': Faculty_member, 'Proposal': Proposal, 'Group': Group, 'Individual report': Individual_report,'Group report': Group_report}
