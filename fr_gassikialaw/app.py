from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_cors import CORS
import mailer
import random
import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.flask import FlaskIntegration

token = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 24))

app = Flask(__name__)
app.secret_key = token
CORS(app)

sentry_sdk.init(
    dsn="https://7a8ff1273de0318966f247225d3bad22@sentry.africantech.dev/3",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    enable_tracing=True,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    integrations = [
        FlaskIntegration(
            transaction_style="url"
        ),
        AioHttpIntegration(
            transaction_style="method_and_path_pattern"
        )
    ]
)

headers = {
    'Content-Type': 'text/html',
    'charset': 'utf-8',
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With",
    "Authorization": "Bearer " + token,
}

@app.route('/', methods=['GET'])
@app.route('/fr_index', methods=['GET'])
def fr_index():
    fr_services = ['Immigration', 'Droit de la famille', 'Droit pénal', 'Droit des affaires', 'Immobilier', 'Planification successorale', 'Dommages corporels', 'Faillite', 'Litige civil', 'Droit du travail' , 'Droit fiscal', 'Autre']
    response = make_response(render_template('fr_index.html', fr_services=fr_services), headers)
    return response


@app.route('/fr_service', methods=['GET'])
def fr_service():
    response = make_response(render_template('fr_service.html'), headers)
    return response

@app.route('/team', methods=['GET'])
def team():
    response = make_response(render_template('team.html'), headers)
    return response


@app.route('/fr_about', methods=['GET'])
def fr_about():
    # services = ['Immigration', 'Family Law', 'Criminal Law', 'Business Law', 'Real Estate', 'Estate Planning', 'Personal Injury', 'Bankruptcy', 'Civil Litigation', 'Employment Law', 'Tax Law', 'Other'] 
    fr_services = ['Immigration', 'Droit de la famille', 'Droit pénal', 'Droit des affaires', 'Immobilier', 'Planification successorale', 'Dommages corporels', 'Faillite', 'Litige civil', 'Droit du travail' , 'Droit fiscal', 'Autre']
    response = make_response(render_template('fr_about.html', fr_services=fr_services), headers)
    return response


@app.route('/fr_contact', methods=['GET', 'POST'])
def fr_contact():
    if request.method == 'POST':
        flash('Your message has been sent successfully!')
        return redirect(url_for('fr_contact'))
    response = make_response(render_template('fr_contact.html'), headers)
    return response

@app.route('/getAppointments', methods=['GET', 'POST'])
def getAppointments():
    if request.method == 'POST':
        full_name = request.form['fullName']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']
        service = request.form.get('services')
        print(full_name, email, date, time, service)
        subject = 'Appointment from ' + full_name
        html_content = f"""
        <htmL>
            <h1>Appointment from {full_name}</h1><br>
            <p>Date: {date}</p>
            <p>Time: {time}</p>
            <p>Services: {service}</p>
            <p>Email was sent from: {email}</p>
        </html>
        """
        try:
            mailer.sendMyEmail('gassikialaw@gmail.com','gassikialaw@gmail.com', subject=subject, msg=html_content)
        except Exception as e:
            print(e)
            pass
        flash('Your Appointment has been sent successfully!')
        return redirect(url_for('fr_index'))
    response = make_response(render_template('fr_index.html'), headers)
    return response

# @app.route('/fr_getAppointments', methods=['GET', 'POST'])
# def fr_getAppointments():
#     if request.method == 'POST':
#         full_name = request.form['fullName']
#         email = request.form['email']
#         date = request.form['date']
#         time = request.form['time']
#         service = request.form.get('services')
#         print(full_name, email, date, time, service)
#         subject = 'Appointment from ' + full_name
#         html_content = f"""
#         <h1>Appointment from {full_name}</h1><br>
#         <p>Date: {date}</p>
#         <p>Time: {time}</p>
#         <p>Services: {service}</p>
#         <p>Email was sent from: {email}</p>
#         """
#         try:
#             mailer.sendMyEmail('Idrisniyi94@gmail.com','gassikialaw@gmail.com', subject=subject, email=email, content=html_content)
#         except Exception as e:
#             print(e)
#             pass
#         flash('Your message has been sent successfully!')
#         return redirect(url_for('fr_home'))
#     response = make_response(render_template('/translate/fr_index.html'), headers)
    return response

@app.route('/contactUs', methods=['GET', 'POST'])
def contactUs():
    error = ''
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        subject = 'Message Enquiry from ' + name
        html_content = f"""
        <h1>Message from {name}</h1><br>
        <p>Email: {email}</p>
        <p>Message: {message}</p>
        """
        try:
            mailer.sendMyEmail('gassikialaw@gmail.com','gassikialaw@gmail.com', subject=subject, msg=html_content)
            error = 'Message sent successfully!'
        except Exception as e:
            print(e)
            pass
        flash('Your message has been sent successfully!')
        return redirect(url_for('contactUs'))
    response = make_response(render_template('fr_contact.html', error=error), headers)
    return response


if __name__ == '__main__':
    app.run(debug=True)


