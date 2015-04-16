# ckanext-lcrnz

CKAN extension for the [Landcare Research Datastore](http://datastore.landcareresearch.co.nz)

## Dependencies

* [ckanext-repeating](https://github.com/open-data/ckanext-repeating)

* [ckanext-ldap](https://github.com/okfn/ckanext-ldap)


## Installation

1. Activate your virtualenv, eg:

        source /usr/lib/ckan/default/bin/activate

2. Install ckanext-repeating:

        cd /usr/lib/ckan/default/src
        git clone https://github.com/open-data/ckanext-repeating.git
        cd ckanext-repeating
        python setup.py develop

3. Install ckanext-ldap:

        # Install required libraries
        apt-get install libldap2-dev libsasl2-dev libssl-dev

        cd /usr/lib/ckan/default/src
        git clone https://github.com/okfn/ckanext-ldap.git
        cd ckanext-ldap
        pip install -r requirements.txt
        python setup.py develop

4. Install ckanext-lcrnz:

        cd /usr/lib/ckan/default/src
        git clone https://github.com/okfn/ckanext-lcrnz.git
        cd ckanext-lcrnz
        python setup.py develop

5. Update the necessary settings in your CKAN config file (by default the
   config file is located at `/etc/ckan/default/production.ini`):

        # ...

        ckan.plugins = repeating lcrnz ldap


        # LDAP settings (adjust uri to the actual one)
        ckanext.ldap.uri = ldap://localhost:389
        ckanext.ldap.base_dn = ou=users,dc=landcareresearch,dc=co,dc=nz
        ckanext.ldap.search.filter = uid={login}
        ckanext.ldap.username = uid
        ckanext.ldap.email = mail
        ckanext.ldap.fullname = cn

        # This is the id of the Landcare Research CKAN organization
        # You can get it from http://datastore.landcareresearch.co.nz/api/action/organization_show?id=landcare-research
        ckanext.ldap.organization.id = cfa490ed-d9e4-46a6-8c43-a7057cfebd1c
        ckanext.ldap.organization.role = member

    The rest of standard settings (`site_id`, `solr_url`, ...) are not covered
    here but should of course be set up as well.

## Development LDAP server

To test the LDAP integration on a development enviroment there is a Docker image
preloaded with a test directory that you can run:

1. [Install docker](http://docs.docker.com/installation/)

2. Run:

        docker run --name ldap -p 389:389 -d openknowledge/openldap-lcrnz

For more details check https://github.com/okfn/docker-openldap-lcrnz


## Customise search field placeholder text

Currently, the placeholder text for the Dataset, Group, and Organization
search fields is blank. Placeholder text can be added by editing the
appropriate `placeholder` variables in `templates/snippets/search_form.html`.
