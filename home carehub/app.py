from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Service provider classes
class ServiceProvider:
    def __init__(self, name, contact_number, service, location):
        self.name = name
        self.contact_number = contact_number
        self.service = service
        self.location = location

    @property
    def info(self):
        return f"{self.service} Provider: {self.name}, Contact: {self.contact_number}, Location: {self.location}"

class Plumber(ServiceProvider):
    def __init__(self, name, contact_number, location):
        super().__init__(name, contact_number, 'Plumber', location)

class Electrician(ServiceProvider):
    def __init__(self, name, contact_number, location):
        super().__init__(name, contact_number, 'Electrician', location)

class ACMechanic(ServiceProvider):
    def __init__(self, name, contact_number, location):
        super().__init__(name, contact_number, 'AC Mechanic', location)

class Laundry(ServiceProvider):
    def __init__(self, name, contact_number, location):
        super().__init__(name, contact_number, 'Laundry', location)

class Housekeeping(ServiceProvider):
    def __init__(self, name, contact_number, location):
        super().__init__(name, contact_number, 'House Keeping', location)

# Initial service provider lists
List_Plumber = [
    Plumber("Leo Das", 9090909090, "Coimbatore North"),
    Plumber("Veera Ragavan", 9090909080, "Coimbatore South"),
    Plumber("Saravana Velu", 9090909070, "Coimbatore West")
]

List_Electrician = [
    Electrician("Abdul Khaliq", 9090909060, "Coimbatore North"),
    Electrician("Vallavan", 9090909050, "Coimbatore South"),
    Electrician("Ethi Rajan", 9090909040, "Coimbatore East")
]

List_ACMechanic = [
    ACMechanic("Anbu", 9090909030, "Coimbatore South"),
    ACMechanic("Kathava Raayan", 9090909020, "Coimbatore West"),
    ACMechanic("Thirchitrambalam", 9090909010, "Coimbatore East")
]

List_Laundry = [
    Laundry("Billa", 9090908090, "Coimbatore North"),
    Laundry("Vinayak Mahadev", 9090908080, "Coimbatore West"),
    Laundry("Sathyadev", 9090908070, "Coimbatore East")
]

List_Housekeeping = [
    Housekeeping("Rolex", 9090908060, "Coimbatore North"),
    Housekeeping("Gajini", 9090908050, "Coimbatore West"),
    Housekeeping("Nedumaran", 9090908040, "Coimbatore South")
]

# Home page route
@app.route('/')
def index():
    registered_provider_info = request.args.get('registered_provider')
    return render_template('index.html', registered_provider=registered_provider_info)

# Register a service provider
@app.route('/register', methods=['POST'])
def register_service():
    name = request.form['name']
    contact = request.form['contact']
    location = request.form['location']
    service_type = request.form['service']

    provider_classes = {
        "Plumber": Plumber,
        "Electrician": Electrician,
        "AC Mechanic": ACMechanic,
        "Laundry": Laundry,
        "House Keeping": Housekeeping
    }

    if service_type in provider_classes:
        provider = provider_classes[service_type](name, contact, location)
        globals()[f'List_{service_type.replace(" ", "")}'].append(provider)

    # Pass the newly registered service provider info back to the index
    return redirect(url_for('index', registered_provider=provider.info))
    print ("REgistration successful")

# View available services
@app.route('/view_services', methods=['POST'])
def view_services():
    service_type = request.form['serviceType']
    location = request.form['location']

    all_providers = List_Plumber + List_Electrician + List_ACMechanic + List_Laundry + List_Housekeeping

    services_found = [provider for provider in all_providers 
                    if provider.service.lower() == service_type.lower() and provider.location.lower() == location.lower()]

    return render_template('index.html', services_found=services_found, service_type=service_type, location=location)
    print (render_template('index.html', services_found=services_found, service_type=service_type, location=location))
# View all registered service providers
@app.route('/view_all_providers')
def view_all_providers():
    all_providers = {
        'Plumbers': List_Plumber,
        'Electricians': List_Electrician,
        'AC Mechanics': List_ACMechanic,
        'Laundry': List_Laundry,
        'Housekeeping': List_Housekeeping
    }
    return render_template('all_providers.html', all_providers=all_providers)

if __name__ == '__main__':
    app.run(debug=True)


