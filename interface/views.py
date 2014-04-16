from flask import render_template #, redirect
from interface import app
from forms import InputForm

def slugify(s):
    return s.lower().replace(' ', '-').replace('/', '').replace('--', '-')

def generate_xls(name_of_app):
    import xlwt

    wb = xlwt.Workbook()

    ws = wb.add_sheet('SKI SSTS')
    ws.write(0, 0, 'SSTS v1')
    ws.write(1, 0, 'www.usatoday.com/experience/' + name_of_app.lower())

    ws = wb.add_sheet('destination nav items')
    ws.write(0, 0, 'DESTINATION')
    for i in range(1, 14):
        ws.write(0, i, 'NAV ITEM %s' % i)
    ws.write(0, 14, 'shopping')
    ws.write(0, 15, 'golfing')
    ws.write(0, 16, 'snorkel scuba')
    ws.write(0, 17, 'NAV ITEM 14')
    ws.write(0, 18, 'NAV ITEM 15')
    ws.write(1, 1, 'Overview')

    fronts = ['FRONT', 'Front Name', 'Parent Front', 'Display Name',
              'Layout Name', 'Platform Type', 'Config', 'Section',
              'Backfill Parent ID', 'Autofill', 'Topic']
    ws = wb.add_sheet('fronts meta')
    for i in range(0, 11):
        ws.write(0, i, fronts[i])
    ws.write(1, 0, 'HOME')
    ws.write(1, 2, 'experience-' + name_of_app.lower())
    ws.write(1, 3, 'Experience ' + name_of_app.capitalize())
    ws.write(1, 4, 'Experience ' + name_of_app.capitalize())
    ws.write(1, 5, 'Web')
    ws.write(1, 6, '<config><item name="ssts" value="experience/{0}" /><item name="texttype" value="section" /><item name="metadescription" value="Build custom {1} travel experiences based on your travel interests. Start planning your trip today, and build the ultimate {0} vacation for you." /><item name="seotitle" value="Experience {1} | USA TODAY Travel" /><item name="canonicalurl" value="http://www.usatoday.com/experience/{0}/" /><item name="keywords" value="{0} travel ideas,{0} vacation guide,{0} experience,travel planning,vacation ideas" /><item name="frontstatus" value="active" /></config>'.format(name_of_app.lower(), name_of_app.capitalize()))
    ws.write(1, 7, 'experience')
    for i in range(8, 11):
        ws.write(1, i, '0')

    wb.save('SSTS Experience %s_v1.xls' % name_of_app.capitalize())

    return "Excel file was successfully generated."

def generate_schema(destinations, tabs):
    f = open("TaxobrowserNavigationSchema", "wb")
    f.write('00000000-0000-0000-0000-000000000000|destinations|\n')
    order = 10
    destinations = destinations.split(',')
    for destination in destinations:
        destination = destination.lstrip()
        f.write('00000000-0000-0000-0000-000000000000|destinations/{0}|url={0},display={1},order={2}\n'.format(slugify(destination), destination, order))
        order += 10
    f.write('00000000-0000-0000-0000-000000000000|destination-tabs|\n')
    order = 10
    tabs = tabs.split(',')
    for tab in tabs:
        tab = tab.lstrip()
        f.write('00000000-0000-0000-0000-000000000000|destination-tabs/{0}|order={2},display={1}\n'.format(slugify(tab), tab, order))
        order += 10
    f.close()

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/input', methods = ['GET', 'POST'])
@app.route('/inputs', methods = ['GET', 'POST'])
def input():
    form = InputForm()
    if form.validate_on_submit():
      # generate_xls(form.name_of_app.data)
        generate_schema(form.destinations.data, form.tabs.data)
        
    return render_template('input.html',
        form = form)
