from app import app, db
from app.models import User,Proposal,Group,Individual_report,Group_report


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Proposal': Proposal, 'Group': Group, 'Individual report': Individual_report,'Group report': Group_report}
