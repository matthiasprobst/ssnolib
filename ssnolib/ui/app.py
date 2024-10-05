from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Get general information
        title = request.form.get('title')
        version = request.form.get('version')
        description = request.form.get('description')

        # Get author information
        authors = []
        first_names = request.form.getlist('first_name[]')
        last_names = request.form.getlist('last_name[]')
        orcids = request.form.getlist('orcid[]')
        emails = request.form.getlist('email[]')

        for first_name, last_name, orcid, email in zip(first_names, last_names, orcids, emails):
            authors.append({
                'first_name': first_name,
                'last_name': last_name,
                'orcid': orcid,
                'email': email
            })

        # Get standard names
        standard_names = []
        names = request.form.getlist('standard_name[]')
        units = request.form.getlist('unit[]')
        name_descriptions = request.form.getlist('name_description[]')

        for name, unit, name_description in zip(names, units, name_descriptions):
            standard_names.append({
                'name': name,
                'unit': unit,
                'description': name_description
            })

        # Get qualifications
        qualifications = []
        qualification_names = request.form.getlist('qualification_name[]')
        valid_values = request.form.getlist('valid_values[]')
        qualification_descriptions = request.form.getlist('qualification_description[]')
        vector_flags = request.form.getlist('vector[]')
        print(qualification_names)
        for name, valid_value, desc, is_vector in zip(qualification_names, valid_values, qualification_descriptions, vector_flags):
            qualifications.append({
                'name': name,
                'valid_value': valid_value,
                'description': desc,
                'is_vector': is_vector == 'on'  # Convert checkbox value to boolean
            })


        # Output the data to check
        return render_template('result.html', title=title, version=version, description=description,
                               authors=authors, standard_names=standard_names, qualifications=qualifications)

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
