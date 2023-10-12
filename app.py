from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample data for job postings
job_postings = []

class JobForm(FlaskForm):
    job_title = StringField('Job Title', validators=[InputRequired()])
    company = StringField('Company', validators=[InputRequired()])
    job_url = StringField('Job URL', validators=[InputRequired()])
    status = SelectField('Status', choices=[('Curious', 'Curious'), ('Applied', 'Applied'), ('Ghosted', 'Ghosted'), ('BOOM!', 'BOOM!')])

@app.route('/')
def list_jobs():
    active_jobs = [job for job in job_postings if job['status'] != 'Archived']
    inactive_jobs = [job for job in job_postings if job['status'] == 'Archived']
    return render_template('list.html', active_jobs=active_jobs, inactive_jobs=inactive_jobs)

@app.route('/create', methods=['GET', 'POST'])
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        job_postings.append({
            'id': len(job_postings),  # Assign a unique ID to each job
            'job_title': form.job_title.data,
            'company': form.company.data,
            'job_url': form.job_url.data,
            'status': form.status.data,
            'created_date': datetime.now().strftime('%m-%d-%Y')
        })
        return redirect(url_for('list_jobs'))
    return render_template('create.html', form=form)

@app.route('/detail/<int:id>', methods=['GET', 'POST'])
def job_detail(id):
    job = next((job for job in job_postings if job['id'] == id), None)
    
    if job is None:
        return redirect(url_for('list_jobs'))
    
    form = JobForm(obj=job)
    
    if request.method == 'POST' and form.validate():
        form.populate_obj(job)
        return redirect(url_for('list_jobs'))
    
    return render_template('detail.html', job=job, form=form)

@app.route('/archive/<int:id>')
def archive_job(id):
    job = next((job for job in job_postings if job['id'] == id), None)
    
    if job is None:
        return redirect(url_for('list_jobs'))
    
    job['status'] = 'Archived'
    return redirect(url_for('list_jobs'))

@app.route('/clear_entries')
def clear_entries():
    job_postings.clear()
    return redirect(url_for('list_jobs'))

if __name__ == '__main__':
    app.run(debug=True)
